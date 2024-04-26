# pylint: disable=ungrouped-imports
import types
from typing import Optional
from typing import Tuple
from typing import Union

import torch
from packaging import version
from torch import nn
from transformers.models.gpt2.modeling_gpt2 import GPT2Attention

from enot_prunable_modules.replace_modules.replacer import Replacer

IS_AMP_AVAILABLE = version.parse(torch.__version__) >= version.parse("1.6")

__all__ = [
    "PrunableGPT2Attention",
    "GPT2AttentionReplacer",
]


class PrunableGPT2Attention(GPT2Attention):
    """Prunable version of GPT2Attention from transformers package."""

    def forward(
        self,
        hidden_states: Optional[Tuple[torch.FloatTensor]],
        layer_past: Optional[Tuple[torch.Tensor]] = None,
        attention_mask: Optional[torch.FloatTensor] = None,
        head_mask: Optional[torch.FloatTensor] = None,
        encoder_hidden_states: Optional[torch.Tensor] = None,
        encoder_attention_mask: Optional[torch.FloatTensor] = None,
        use_cache: Optional[bool] = False,
        output_attentions: Optional[bool] = False,
    ) -> Tuple[Union[torch.Tensor, Tuple[torch.Tensor]], ...]:
        """Replace split with slice."""
        batch_size, seq_len, _ = hidden_states.shape
        if encoder_hidden_states is not None:
            if not hasattr(self, "q_attn"):
                raise ValueError(
                    "If class is used as cross attention, the weights `q_attn` have to be defined. "
                    "Please make sure to instantiate class with `GPT2Attention(..., is_cross_attention=True)`."
                )

            query = self.q_attn(hidden_states)
            key_value = self.c_attn(encoder_hidden_states)
            query = query.reshape(batch_size, seq_len, self.num_heads, self.head_dim).transpose(1, 2)
            key_value = key_value.reshape(batch_size, seq_len, 2, self.num_heads, self.head_dim).permute(2, 0, 3, 1, 4)
            key, value = key_value[0], key_value[1]
            attention_mask = encoder_attention_mask
        else:
            qkv = self.c_attn(hidden_states)
            qkv = qkv.reshape(batch_size, seq_len, 3, self.num_heads, self.head_dim).permute(2, 0, 3, 1, 4)
            query, key, value = qkv[0], qkv[1], qkv[2]

        if layer_past is not None:
            past_key, past_value = layer_past  # type: ignore
            key = torch.cat((past_key, key), dim=-2)
            value = torch.cat((past_value, value), dim=-2)

        if use_cache is True:
            present = (key, value)
        else:
            present = None

        if self.reorder_and_upcast_attn:
            attn_output, attn_weights = self._upcast_and_reordered_attn(query, key, value, attention_mask, head_mask)
        else:
            attn_output, attn_weights = self._attn(query, key, value, attention_mask, head_mask)

        attn_output = attn_output.transpose(1, 2).flatten(2)
        attn_output = self.c_proj(attn_output)
        attn_output = self.resid_dropout(attn_output)

        outputs = (attn_output, present)
        if output_attentions:
            outputs += (attn_weights,)

        return outputs  # a, present, (attentions)

    def _attn(self, query, key, value, attention_mask=None, head_mask=None):
        """Replace torch.where for causal mask with sum and product."""
        attn_weights = torch.matmul(query, key.transpose(-1, -2))

        if self.scale_attn_weights:
            attn_weights = attn_weights / torch.full(
                [], value.size(-1) ** 0.5, dtype=attn_weights.dtype, device=attn_weights.device
            )

        # Layer-wise attention scaling
        if self.scale_attn_by_inverse_layer_idx:
            attn_weights = attn_weights / float(self.layer_idx + 1)

        if not self.is_cross_attention:
            # if only "normal" attention layer implements causal mask
            query_length, key_length = query.size(-2), key.size(-2)
            causal_mask = self.bias[:, :, key_length - query_length : key_length, :key_length]
            mask_value = torch.finfo(attn_weights.dtype).min
            # Need to be a tensor, otherwise we get error: `RuntimeError: expected scalar type float but found double`.
            # Need to be on the same device, otherwise `RuntimeError: ..., x and y to be on the same device`
            mask_value = torch.full([], mask_value, dtype=attn_weights.dtype, device=attn_weights.device)
            attn_weights = causal_mask * attn_weights + (~causal_mask) * mask_value  # << enot fixed

        if attention_mask is not None:
            # Apply the attention mask
            attn_weights = attn_weights + attention_mask

        attn_weights = nn.functional.softmax(attn_weights, dim=-1)

        # Downcast (if necessary) back to V's dtype (if in mixed-precision) -- No-Op otherwise
        attn_weights = attn_weights.type(value.dtype)
        attn_weights = self.attn_dropout(attn_weights)

        # Mask heads if we want to
        if head_mask is not None:
            attn_weights = attn_weights * head_mask

        attn_output = torch.matmul(attn_weights, value)

        return attn_output, attn_weights


class GPT2AttentionReplacer(Replacer):
    """GPT2Attention module replacer."""

    def replace(self, module: GPT2Attention) -> None:
        """Replace GPT2Attention module inplace with its prunable version."""
        module.forward = types.MethodType(PrunableGPT2Attention.forward, module)
        module.__class__ = PrunableGPT2Attention

    def revert(self, module: PrunableGPT2Attention) -> None:
        """Revert prunable version to original one."""
        module.forward = types.MethodType(GPT2Attention.forward, module)
        module.__class__ = GPT2Attention

        module.split_size = module.num_heads * module.head_dim
