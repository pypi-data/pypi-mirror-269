import math
import warnings
from functools import partial
from typing import Dict
from typing import Tuple
from typing import Type

import torch
from timm.models.levit import Attention as LeViTAttention
from timm.models.levit import AttentionSubsample as LeViTAttentionSubsample
from timm.models.levit import ConvNorm
from timm.models.levit import LinearNorm
from timm.models.levit import Subsample
from torch import nn

from enot_prunable_modules.replace_modules.replacer import Replacer

__all__ = [
    "PrunableLeViTAttentionSubsample",
    "PrunableLeViTAttention",
    "LeViTAttentionSubsampleReplacer",
    "LeViTAttentionReplacer",
]


class PrunableLeViTAttention(nn.Module):
    """timm.models.levit.Attention."""

    attention_biases_cache: Dict[str, torch.Tensor]  # per-device attention_biases cache

    def __init__(
        self,
        dim: int,
        key_dim: int,
        num_heads: int = 8,
        attn_ratio: int = 4,
        act_layer: Type[nn.Module] = nn.SiLU,
        resolution: int = 14,
        use_conv: bool = False,
    ):
        """Add self.double_key_dim, remove self.key_attn_dim` and `self.val_dim`."""
        super().__init__()
        ln_layer = ConvNorm if use_conv else LinearNorm
        self.use_conv = use_conv
        self.num_heads = num_heads
        self.scale = key_dim**-0.5
        self.key_dim = key_dim
        # Modification: added `self.double_key_dim`.
        self.double_key_dim = key_dim * 2
        # Modification: remove `self.key_attn_dim` and `self.val_dim` because
        # their values will be invalid after pruning.
        self.val_attn_dim = int(attn_ratio * key_dim) * num_heads

        self.qkv = ln_layer(dim, int(self.val_attn_dim + key_dim * num_heads * 2), resolution=resolution)
        self.proj = nn.Sequential(
            act_layer(),
            ln_layer(self.val_attn_dim, dim, bn_weight_init=0, resolution=resolution),
        )

        self.attention_biases = nn.Parameter(torch.zeros(num_heads, resolution**2))
        pos = torch.stack(torch.meshgrid(torch.arange(resolution), torch.arange(resolution))).flatten(1)
        rel_pos = (pos[..., :, None] - pos[..., None, :]).abs()
        rel_pos = (rel_pos[0] * resolution) + rel_pos[1]
        self.register_buffer("attention_bias_idxs", rel_pos)
        self.attention_biases_cache = {}

    @torch.no_grad()
    def train(self, mode=True):
        """Nothing changed."""
        super().train(mode)
        if mode and self.attention_biases_cache:
            self.attention_biases_cache = {}  # clear attention_biases cache

    def get_attention_biases(self, device: torch.device) -> torch.Tensor:
        """Nothing changed."""
        if self.training:
            return self.attention_biases[:, self.attention_bias_idxs]

        device_key = str(device)
        if device_key not in self.attention_biases_cache:
            self.attention_biases_cache[device_key] = self.attention_biases[:, self.attention_bias_idxs]
        return self.attention_biases_cache[device_key]

    def forward(self, input_tensor) -> torch.Tensor:  # input_tensor (batch_size, channels, height, width)
        """Remove channel accessing, replace split with slice."""
        if self.use_conv:
            # Modification: replaced `batch_size, channels, height, width = input_tensor.shape`
            # with `batch_size, _, height, width = input_tensor.shape`.
            batch_size, _, height, width = input_tensor.shape
            qkv = self.qkv(input_tensor).view(batch_size, self.num_heads, -1, height * width)
            # Modification: replace split with slicing. Use slices with values directly from self
            # to help integer tracing.
            query = qkv[..., : self.key_dim, :]
            key = qkv[..., self.key_dim : self.double_key_dim, :]
            value = qkv[..., self.double_key_dim :, :]

            attn = (query.transpose(-2, -1) @ key) * self.scale + self.get_attention_biases(input_tensor.device)
            attn = attn.softmax(dim=-1)

            input_tensor = (value @ attn.transpose(-2, -1)).view(batch_size, -1, height, width)
        else:
            # Modification: replaced `batch_size, seq_len, channels = input_tensor.shape`
            # with `batch_size, seq_len, _ = input_tensor.shape`.
            batch_size, seq_len, _ = input_tensor.shape
            qkv = self.qkv(input_tensor).view(batch_size, seq_len, self.num_heads, -1)
            # Modification: replaced split with slicing. Use slices with values directly from self
            # to help integer tracing.
            query = qkv[..., : self.key_dim]
            key = qkv[..., self.key_dim : self.double_key_dim]
            value = qkv[..., self.double_key_dim :]
            query = query.permute(0, 2, 1, 3)
            key = key.permute(0, 2, 3, 1)
            value = value.permute(0, 2, 1, 3)

            attn = query @ key * self.scale + self.get_attention_biases(input_tensor.device)
            attn = attn.softmax(dim=-1)

            input_tensor = (attn @ value).transpose(1, 2).reshape(batch_size, seq_len, self.val_attn_dim)
        input_tensor = self.proj(input_tensor)
        return input_tensor


class PrunableLeViTAttentionSubsample(nn.Module):
    """timm.models.levit.AttentionSubsample."""

    attention_biases_cache: Dict[str, torch.Tensor]  # per-device attention_biases cache

    def __init__(
        self,
        in_dim: int,
        out_dim: int,
        key_dim: int,
        num_heads: int = 8,
        attn_ratio: int = 2,
        act_layer: nn.Module = None,
        stride: int = 2,
        resolution: int = 14,
        resolution_out: int = 7,
        use_conv: bool = False,
    ):
        """Nothing changed."""
        super().__init__()
        self.stride = stride
        self.num_heads = num_heads
        self.scale = key_dim**-0.5
        self.key_dim = key_dim
        self.key_attn_dim = key_dim * num_heads
        self.val_dim = int(attn_ratio * key_dim)
        self.val_attn_dim = self.val_dim * self.num_heads
        self.resolution = resolution
        self.resolution_out_area = resolution_out**2

        self.use_conv = use_conv
        if self.use_conv:
            ln_layer = ConvNorm
            sub_layer = partial(nn.AvgPool2d, kernel_size=1, padding=0)
        else:
            ln_layer = LinearNorm
            sub_layer = partial(Subsample, resolution=resolution)
        self.kv = ln_layer(  # pylint: disable=C0103
            in_dim, self.val_attn_dim + self.key_attn_dim, resolution=resolution
        )
        self.q = nn.Sequential(  # pylint: disable=C0103
            sub_layer(stride=stride),
            ln_layer(in_dim, self.key_attn_dim, resolution=resolution_out),
        )
        self.proj = nn.Sequential(
            act_layer(),
            ln_layer(self.val_attn_dim, out_dim, resolution=resolution_out),
        )

        self.attention_biases = nn.Parameter(torch.zeros(num_heads, self.resolution**2))
        k_pos = torch.stack(torch.meshgrid(torch.arange(resolution), torch.arange(resolution))).flatten(1)
        q_pos = torch.stack(
            torch.meshgrid(torch.arange(0, resolution, step=stride), torch.arange(0, resolution, step=stride))
        ).flatten(1)
        rel_pos = (q_pos[..., :, None] - k_pos[..., None, :]).abs()
        rel_pos = (rel_pos[0] * resolution) + rel_pos[1]
        self.register_buffer("attention_bias_idxs", rel_pos)

        self.attention_biases_cache = {}  # per-device attention_biases cache

    @torch.no_grad()
    def train(self, mode=True):
        """Nothing changed."""
        super().train(mode)
        if mode and self.attention_biases_cache:
            self.attention_biases_cache = {}  # clear attention_biases_cache

    def get_attention_biases(self, device: torch.device) -> torch.Tensor:
        """Nothing changed."""
        if self.training:
            return self.attention_biases[:, self.attention_bias_idxs]

        device_key = str(device)
        if device_key not in self.attention_biases_cache:
            self.attention_biases_cache[device_key] = self.attention_biases[:, self.attention_bias_idxs]
        return self.attention_biases_cache[device_key]

    def forward(self, input_tensor) -> torch.Tensor:
        """Remove channel accessing, replace split with slice."""
        if self.use_conv:
            # Modification: replaced `batch_size, channels, height, width = input_tensor.shape`
            # with `batch_size, _, height, width = input_tensor.shape`.
            batch_size, _, height, width = input_tensor.shape
            key_and_value = self.kv(input_tensor).view(batch_size, self.num_heads, -1, height * width)
            query = self.q(input_tensor).view(batch_size, self.num_heads, self.key_dim, self.resolution_out_area)
            # Modification: replaced split with slicing. Use slices with values directly from self
            # to help integer tracing.
            key = key_and_value[..., : self.key_dim, :]
            value = key_and_value[..., self.key_dim :, :]

            attn = (query.transpose(-2, -1) @ key) * self.scale + self.get_attention_biases(input_tensor.device)
            attn = attn.softmax(dim=-1)

            input_tensor = (value @ attn.transpose(-2, -1)).reshape(batch_size, -1, self.resolution, self.resolution)
        else:
            # Modification: replaced `batch_size, seq_len, channels = input_tensor.shape`
            # with `batch_size, seq_len, _ = input_tensor.shape`.
            batch_size, seq_len, _ = input_tensor.shape
            key_and_value = self.kv(input_tensor).view(batch_size, seq_len, self.num_heads, -1)
            # Modification: replaced split with slicing. Use slices with values directly from self
            # to help integer tracing.
            key = key_and_value[..., : self.key_dim]
            value = key_and_value[..., self.key_dim :]
            key = key.permute(0, 2, 3, 1)  # BHCN
            value = value.permute(0, 2, 1, 3)  # BHNC
            query = (
                self.q(input_tensor)
                .view(batch_size, self.resolution_out_area, self.num_heads, self.key_dim)
                .permute(0, 2, 1, 3)
            )

            attn = query @ key * self.scale + self.get_attention_biases(input_tensor.device)
            attn = attn.softmax(dim=-1)

            input_tensor = (attn @ value).transpose(1, 2).reshape(batch_size, -1, self.val_attn_dim)
        input_tensor = self.proj(input_tensor)
        return input_tensor


class LeViTAttentionReplacer(Replacer):
    """
    LeViTAttention module replacer.

    Replacing module forever. Revert method does nothing.

    """

    def replace(self, module: LeViTAttention) -> PrunableLeViTAttention:
        """Replace LeViTAttention module with its prunable version."""
        dim: int = _get_in_out_features_from_ln_layer(module.qkv)[0]
        val_dim: int = module.val_dim if hasattr(module, "val_dim") else module.d
        attn_ratio = val_dim // module.key_dim
        resolution = int(math.sqrt(module.attention_bias_idxs.shape[1]) + 0.5)

        attn = PrunableLeViTAttention(
            dim=dim,
            key_dim=module.key_dim,
            num_heads=module.num_heads,
            attn_ratio=attn_ratio,
            act_layer=lambda: module.proj[0],  # type: ignore
            resolution=resolution,
            use_conv=module.use_conv,
        )
        attn.qkv.c.weight = module.qkv.c.weight
        attn.qkv.bn.weight = module.qkv.bn.weight
        attn.qkv.bn.bias = module.qkv.bn.bias

        attn.proj = module.proj
        attn.attention_biases = module.attention_biases
        attn.attention_biases_cache = module.ab

        return attn

    def revert(self, module: PrunableLeViTAttention) -> None:
        """Do nothing."""


class LeViTAttentionSubsampleReplacer(Replacer):
    """
    LeViTAttentionSubsample module replacer.

    Replacing module forever. Revert method does nothing.

    """

    def replace(self, module: LeViTAttentionSubsample) -> PrunableLeViTAttentionSubsample:
        """Replace LeViTAttentionSubsample module with its prunable version."""
        in_dim: int = _get_in_out_features_from_ln_layer(module.kv)[0]
        out_dim: int = _get_in_out_features_from_ln_layer(module.proj[1])[1]
        val_dim: int = module.val_dim if hasattr(module, "val_dim") else module.d
        attn_ratio: int = val_dim // module.key_dim
        resolution: int = int(math.sqrt(module.attention_bias_idxs.shape[1]) + 0.5)
        if hasattr(module, "resolution_"):
            resolution_out: int = module.resolution_
        else:
            resolution_out: int = int(math.sqrt(module.resolution_out_area) + 0.5)

        attn = PrunableLeViTAttentionSubsample(
            in_dim=in_dim,
            out_dim=out_dim,
            key_dim=module.key_dim,
            num_heads=module.num_heads,
            attn_ratio=attn_ratio,
            act_layer=lambda: module.proj[0],
            stride=module.stride,
            resolution=resolution,
            resolution_out=resolution_out,
            use_conv=module.use_conv,
        )
        attn.kv = module.kv
        attn.q = module.q
        attn.proj = module.proj
        attn.attention_biases_cache = module.ab

        return attn

    def revert(self, module: PrunableLeViTAttentionSubsample) -> None:
        """Do nothing."""
        warnings.warn(
            f"{type(module)} reverting is not implemented yet or it is impossible to implement.",
            UserWarning,
        )


def _get_in_out_features_from_ln_layer(ln_layer: torch.nn.Module) -> Tuple[int, int]:
    weight_layer = ln_layer.c
    is_linear = isinstance(weight_layer, torch.nn.Linear)
    if is_linear:
        return weight_layer.in_features, weight_layer.out_features

    return weight_layer.in_channels, weight_layer.out_channels
