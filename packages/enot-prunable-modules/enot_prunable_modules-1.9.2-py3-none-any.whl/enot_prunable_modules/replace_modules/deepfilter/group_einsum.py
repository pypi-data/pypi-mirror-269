import types

import torch
from df.modules import GroupedLinearEinsum

from enot_prunable_modules.replace_modules.replacer import Replacer

__all__ = [
    "PrunableGroupedLinearEinsum",
    "GroupedLinearEinsumReplacer",
]


class PrunableGroupedLinearEinsum(GroupedLinearEinsum):
    """
    Prunable version of forward.

    Be careful! There are __repr__ problems for replaced and pruned module.

    """

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Remove einsum and rewrite like group operation."""
        groups = []
        for idx in range(self.groups):
            matmul_res = x[:, :, : self.ws] @ self.weight[idx]
            groups.append(matmul_res)
            x = x[:, :, self.ws :]
        x = torch.cat(groups, dim=2)
        return x


class GroupedLinearEinsumReplacer(Replacer):
    """GroupedLinearEinsum module replacer."""

    def replace(self, module: GroupedLinearEinsum) -> None:
        """Replace GroupedLinearEinsum module inplace with its prunable version."""
        module.forward = types.MethodType(PrunableGroupedLinearEinsum.forward, module)
        module.__class__ = PrunableGroupedLinearEinsum

    def revert(self, module: PrunableGroupedLinearEinsum) -> None:
        """Revert GroupedLinearEinsum module replacing."""
        module.__class__ = GroupedLinearEinsum
        module.forward = types.MethodType(GroupedLinearEinsum.forward, module)

        # Fix __repr__ after replacing and pruning
        module.input_size = module.weight.shape[0] * module.weight.shape[1]
        module.hidden_size = module.weight.shape[0] * module.weight.shape[2]
        module.groups = module.weight.shape[0]
