import types
import warnings

from torch.nn import GLU
from torch.nn.functional import sigmoid

from enot_prunable_modules.replace_modules.replacer import Replacer

__all__ = [
    "PrunableGLU",
    "GLUReplacer",
]


class PrunableGLU(GLU):
    """torch.nn.GLU."""

    def forward(self, input):  # pylint: disable=W0622
        """Use permute and reshape to split matrix."""
        window, _, seq_length = input.shape
        channel_last = input.permute((0, 2, 1))
        chunk = channel_last.reshape((window, seq_length, 2, -1))
        weights, to_sigmoid = chunk[..., 0, :], chunk[..., 1, :]
        res = weights * sigmoid(to_sigmoid)
        res = res.permute(0, 2, 1)
        return res


class GLUReplacer(Replacer):
    """GLU module replacer."""

    def replace(self, module: GLU) -> None:
        """Replace GLU module inplace with its prunable version."""
        if module.dim == 1:
            module.forward = types.MethodType(PrunableGLU.forward, module)
            module.__class__ = PrunableGLU
        else:
            warnings.warn("torch.nn.GLU implemented only for the first dimension.")

    def revert(self, module: PrunableGLU) -> None:
        """Revert GLU module replacing."""
        module.forward = types.MethodType(GLU.forward, module)
        module.__class__ = GLU
