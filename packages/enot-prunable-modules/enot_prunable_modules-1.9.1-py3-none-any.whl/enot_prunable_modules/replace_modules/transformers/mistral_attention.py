import math
import types
from typing import Optional
from typing import Tuple

import torch
from torch import nn
from transformers.models.mistral.modeling_mistral import MistralAttention

from enot_prunable_modules.replace_modules.replacer import Replacer

__all__ = [
    "PrunableMistralAttention",
    "MistralAttentionReplacer",
]


class PrunableMistralAttention(MistralAttention):
    """Prunable version of MistralAttention from transformers package."""

    def forward(
        self,
        hidden_states: torch.Tensor,
        attention_mask: Optional[torch.Tensor] = None,
        position_ids: Optional[torch.LongTensor] = None,
        past_key_value: Optional[Tuple[torch.Tensor, torch.Tensor]] = None,
        output_attentions: bool = False,
        use_cache: bool = False,
        **kwargs,
    ) -> Tuple[torch.Tensor, Optional[torch.Tensor], Optional[Tuple[torch.Tensor, torch.Tensor]]]:
        """Change rotary positional embedding computation to prunable version."""
        bsz, q_len, _ = hidden_states.shape

        query_states = self.q_proj(hidden_states)
        key_states = self.k_proj(hidden_states)
        value_states = self.v_proj(hidden_states)

        query_states = query_states.view(bsz, q_len, self.num_heads, self.head_dim).transpose(1, 2)
        key_states = key_states.view(bsz, q_len, self.num_key_value_heads, self.head_dim).transpose(1, 2)
        value_states = value_states.view(bsz, q_len, self.num_key_value_heads, self.head_dim).transpose(1, 2)

        # Force linears to the same shape according to original implementation
        query_states = query_states * self.parameter.view(1, 1, 1, -1)
        key_states = key_states * self.parameter.view(1, 1, 1, -1)
        value_states = value_states * self.parameter.view(1, 1, 1, -1)

        kv_seq_len = key_states.shape[-2]
        if past_key_value is not None:
            kv_seq_len += past_key_value[0].shape[-2]
        cos, sin = self.rotary_emb(value_states, seq_len=kv_seq_len)
        query_states, key_states = _apply_rotary_pos_emb(
            q=query_states,
            k=key_states,
            cos=cos,
            sin=sin,
            position_ids=position_ids,
            rotary_ndims_half=self.rotary_ndims_half,
        )

        if past_key_value is not None:
            # reuse k, v, self_attention
            key_states = torch.cat([past_key_value[0], key_states], dim=2)
            value_states = torch.cat([past_key_value[1], value_states], dim=2)

        past_key_value = (key_states, value_states) if use_cache else None

        # repeat k/v heads if n_kv_heads < n_heads
        key_states = _repeat_kv(key_states, self.num_key_value_groups)
        value_states = _repeat_kv(value_states, self.num_key_value_groups)

        attn_weights = torch.matmul(query_states, key_states.transpose(2, 3)) / math.sqrt(self.head_dim)

        if attn_weights.size() != (bsz, self.num_heads, q_len, kv_seq_len):
            raise ValueError(
                f"Attention weights should be of size {(bsz, self.num_heads, q_len, kv_seq_len)}, but is"
                f" {attn_weights.size()}"
            )

        if attention_mask is not None:
            if attention_mask.size() != (bsz, 1, q_len, kv_seq_len):
                raise ValueError(
                    f"Attention mask should be of size {(bsz, 1, q_len, kv_seq_len)}, but is {attention_mask.size()}"
                )

            attn_weights = attn_weights + attention_mask

        # upcast attention to fp32
        attn_weights = nn.functional.softmax(attn_weights, dim=-1, dtype=torch.float32).to(query_states.dtype)
        attn_output = torch.matmul(attn_weights, value_states)

        if attn_output.size() != (bsz, self.num_heads, q_len, self.head_dim):
            raise ValueError(
                f"`attn_output` should be of size {(bsz, self.num_heads, q_len, self.head_dim)}, but is"
                f" {attn_output.size()}"
            )

        attn_output = attn_output.transpose(1, 2).contiguous()
        attn_output = attn_output.reshape(bsz, q_len, self.hidden_size)

        attn_output = self.o_proj(attn_output)

        if not output_attentions:
            attn_weights = None

        return attn_output, attn_weights, past_key_value


class MistralAttentionReplacer(Replacer):
    """MistralAttention module replacer."""

    # pylint: disable=W0212
    def replace(self, module: MistralAttention) -> None:
        """Replace MistralAttention module inplace with its prunable version."""
        module.forward = types.MethodType(PrunableMistralAttention.forward, module)
        module.__class__ = PrunableMistralAttention

        setattr(module, "rotary_ndims_half", module.head_dim // 2)
        setattr(module, "parameter", nn.Parameter(torch.ones(module.head_dim)))

    # pylint: disable=W0212
    def revert(self, module: PrunableMistralAttention) -> None:
        """Revert prunable version to original one."""
        module.forward = types.MethodType(MistralAttention.forward, module)
        module.__class__ = MistralAttention

        delattr(module, "rotary_ndims_half")
        delattr(module, "parameter")


def _rotate_half(x, rotary_ndims_half: int):
    """Add rotary_ndims_half for prunable slice."""
    x1 = x[..., :rotary_ndims_half]
    x2 = x[..., rotary_ndims_half:]
    return torch.cat((-x2, x1), dim=-1)


def _apply_rotary_pos_emb(q, k, cos, sin, position_ids, rotary_ndims_half: int, unsqueeze_dim=1):
    """Add rotary_ndims_half for prunable rotate_half."""
    cos = cos[position_ids].unsqueeze(unsqueeze_dim)
    sin = sin[position_ids].unsqueeze(unsqueeze_dim)

    q_embed = (q * cos) + (_rotate_half(q, rotary_ndims_half) * sin)
    k_embed = (k * cos) + (_rotate_half(k, rotary_ndims_half) * sin)

    return q_embed, k_embed


def _repeat_kv(hidden_states: torch.Tensor, n_rep: int) -> torch.Tensor:
    """Replace torch.expand to torch.cat."""
    _, num_key_value_heads, _, _ = hidden_states.shape

    if n_rep == 1:
        return hidden_states

    hidden_states_list = []
    for key_value_head_idx in range(num_key_value_heads):
        for _ in range(n_rep):
            hidden_states_list.append(hidden_states[:, key_value_head_idx, :, :].unsqueeze(1))
    return torch.cat(hidden_states_list, dim=1)
