"""Custom normalization layers."""
from typing import Optional, Tuple, Union

import torch
import torch.nn as nn

from vllm._C import ops


class SmoothQuantRMSNorm(nn.Module):
    """Root mean square normalization in SmoothQuant input_layernorm.
    It applies RMS normalization on x then quantizes outputs into int8.

    Computes x -> w * x / sqrt(E[x^2] + eps) where w is the learned weight.
    Refer to https://arxiv.org/abs/1910.07467
    """

    def __init__(
        self,
        hidden_size: int,
        eps: float = 1e-6,
    ) -> None:
        super().__init__()
        self.weight = nn.Parameter(torch.ones(hidden_size))
        self.variance_epsilon = eps

    def _forward(
        self,
        x: torch.Tensor,
    ) -> Union[torch.Tensor, Tuple[torch.Tensor, torch.Tensor]]:
        """PyTorch-native implementation equivalent to forward()."""
        orig_dtype = x.dtype
        x = x.to(torch.float32)
        variance = x.pow(2).mean(dim=-1, keepdim=True)
        x = x * torch.rsqrt(variance + self.variance_epsilon)
        x = x.to(orig_dtype) * self.weight
        return x

    def forward(
        self,
        x: torch.Tensor,
    ) -> Union[torch.Tensor, Tuple[torch.Tensor, torch.Tensor]]:
        # return self._forward(x)

        out = torch.empty_like(x, dtype=torch.int8)

        per_token_shape = list(x.size())
        per_token_shape[-1] = 1
        dyn_scale = torch.empty(per_token_shape, dtype=torch.float, device=x.device)

        ops.smoothquant_rms_norm(out, dyn_scale, x, self.weight.data, self.variance_epsilon)

        # [TODO]: return int8 for sq matmul
        # res = out * dyn_scale
        # res = res.to(x.dtype)
        # return res

        return out, dyn_scale
