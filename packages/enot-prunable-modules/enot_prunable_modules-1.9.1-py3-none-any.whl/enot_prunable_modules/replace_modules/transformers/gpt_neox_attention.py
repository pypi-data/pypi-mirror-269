import types
from typing import Optional
from typing import Tuple

import torch
from transformers.models.gpt_neox.modeling_gpt_neox import GPTNeoXAttention

from enot_prunable_modules.replace_modules.replacer import Replacer

__all__ = [
    "PrunableGPTNeoXAttention",
    "GPTNeoXAttentionReplacer",
]


class PrunableGPTNeoXAttention(GPTNeoXAttention):
    """Prunable version of GPTNeoXAttention from transformers package."""

    def forward(
        self,
        hidden_states: torch.FloatTensor,
        attention_mask: torch.FloatTensor,
        position_ids: torch.LongTensor,
        head_mask: Optional[torch.FloatTensor] = None,
        layer_past: Optional[Tuple[torch.Tensor, torch.Tensor]] = None,
        use_cache: Optional[bool] = False,
        output_attentions: Optional[bool] = False,
    ):
        """Replace query, key, value computation to prunable version."""
        has_layer_past = layer_past is not None

        batch_size, inp_seq_len, _ = hidden_states.shape

        # Compute QKV
        qkv = self.query_key_value(hidden_states)
        qkv = qkv.reshape(batch_size, inp_seq_len, self.num_attention_heads, 3, self.head_size).permute(3, 0, 2, 1, 4)
        query, key, value = qkv[0], qkv[1], qkv[2]

        # Compute rotary embeddings on rotary_ndims
        query_rot = query[..., : self.rotary_ndims]
        query_pass = query[..., self.rotary_ndims :]
        key_rot = key[..., : self.rotary_ndims]
        key_pass = key[..., self.rotary_ndims :]

        # Compute token offset for rotary embeddings (when decoding)
        seq_len = key.shape[-2]
        if has_layer_past:
            seq_len += layer_past[0].shape[-2]
        cos, sin = self.rotary_emb(value, seq_len=seq_len)
        query, key = _apply_rotary_pos_emb(query_rot, key_rot, cos, sin, position_ids, self.rotary_ndims_half)
        query = torch.cat((query, query_pass), dim=-1)
        key = torch.cat((key, key_pass), dim=-1)

        # Cache QKV values
        if has_layer_past:
            past_key = layer_past[0]
            past_value = layer_past[1]
            key = torch.cat((past_key, key), dim=-2)
            value = torch.cat((past_value, value), dim=-2)
        present = (key, value) if use_cache else None

        # Compute attention
        attn_output, attn_weights = self._attn(query, key, value, attention_mask, head_mask)

        # Reshape outputs
        attn_output = attn_output.permute(0, 2, 1, 3).contiguous()
        attn_output = attn_output.reshape(batch_size, inp_seq_len, -1)
        attn_output = self.dense(attn_output)

        outputs = (attn_output, present)
        if output_attentions:
            outputs += (attn_weights,)

        return outputs

    def _attn(self, query, key, value, attention_mask=None, head_mask=None):
        """Replace to prunable version."""
        attn_scores = (query @ key.transpose(-2, -1)) * self.norm_factor

        # compute causal mask from causal mask buffer
        query_length, key_length = query.size(-2), key.size(-2)

        # dynamically increase the causal mask with the key length, if needed.
        if key_length > self.bias.shape[-1]:
            self._init_bias(key_length, device=key.device)
        causal_mask = self.bias[:, :, key_length - query_length : key_length, :key_length].to(torch.bool)

        mask_value = torch.finfo(attn_scores.dtype).min
        # Need to be a tensor, otherwise we get error: `RuntimeError: expected scalar type float but found double`.
        # Need to be on the same device, otherwise `RuntimeError: ..., x and y to be on the same device`
        mask_value = torch.tensor(mask_value, dtype=attn_scores.dtype).to(attn_scores.device)
        attn_scores = attn_scores * causal_mask + (~causal_mask) * mask_value

        if attention_mask is not None:
            # Apply the attention mask
            attn_scores = attn_scores + attention_mask

        attn_weights = attn_scores.softmax(dim=-1)
        attn_weights = attn_weights.to(value.dtype)

        # Mask heads if we want to
        if head_mask is not None:
            attn_weights = attn_weights * head_mask

        attn_weights = self.attention_dropout(attn_weights)

        attn_output = torch.matmul(attn_weights, value)
        return attn_output, attn_weights


class GPTNeoXAttentionReplacer(Replacer):
    """GPTNeoXAttention module replacer."""

    # pylint: disable=W0212
    def replace(self, module: GPTNeoXAttention) -> None:
        """Replace GPTNeoXAttention module inplace with its prunable version."""
        module.forward = types.MethodType(PrunableGPTNeoXAttention.forward, module)
        module._attn = types.MethodType(PrunableGPTNeoXAttention._attn, module)
        module.__class__ = PrunableGPTNeoXAttention

        setattr(module, "rotary_ndims_half", module.rotary_ndims // 2)

    # pylint: disable=W0212
    def revert(self, module: PrunableGPTNeoXAttention) -> None:
        """Revert prunable version to original one."""
        module.forward = types.MethodType(GPTNeoXAttention.forward, module)
        module._attn = types.MethodType(GPTNeoXAttention._attn, module)
        module.__class__ = GPTNeoXAttention

        delattr(module, "rotary_ndims_half")


def _rotate_half(x, rotary_ndims_half):
    """Add rotary_ndims_half for prunable slice."""
    x1 = x[..., :rotary_ndims_half]
    x2 = x[..., rotary_ndims_half:]
    return torch.cat((-x2, x1), dim=-1)


def _apply_rotary_pos_emb(q, k, cos, sin, position_ids, rotary_ndims_half, unsqueeze_dim=1):
    """Add rotary_ndims_half for prunable rotate_half."""
    cos = cos[position_ids].unsqueeze(unsqueeze_dim)
    sin = sin[position_ids].unsqueeze(unsqueeze_dim)

    q_embed = (q * cos) + (_rotate_half(q, rotary_ndims_half) * sin)
    k_embed = (k * cos) + (_rotate_half(k, rotary_ndims_half) * sin)

    return q_embed, k_embed
