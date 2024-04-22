r"""Contain the computation models."""

from __future__ import annotations

__all__ = [
    "ArrayComputationModel",
    "BaseComputationModel",
    "MaskedArrayComputationModel",
    "AutoComputationModel",
    "argmax",
    "argmin",
    "argsort",
    "concatenate",
    "max",
    "mean",
    "median",
    "min",
    "sort",
    "register_computation_models",
]

from batcharray.computation.array import ArrayComputationModel
from batcharray.computation.auto import (
    AutoComputationModel,
    register_computation_models,
)
from batcharray.computation.base import BaseComputationModel
from batcharray.computation.interface import (
    argmax,
    argmin,
    argsort,
    concatenate,
    max,
    mean,
    median,
    min,
    sort,
)
from batcharray.computation.masked_array import MaskedArrayComputationModel

register_computation_models()
