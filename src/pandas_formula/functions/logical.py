"""Logical functions."""

import numpy as np

from .registry import FunctionRegistry


def register_logical_functions(registry: FunctionRegistry) -> None:
    """Register logical functions."""

    registry.register("and_", lambda a, b: a & b, "Logical AND: @and_(a, b)")
    registry.register("or_", lambda a, b: a | b, "Logical OR: @or_(a, b)")
    registry.register("not_", lambda a: ~a, "Logical NOT: @not_(a)")
    registry.register(
        "if_else",
        lambda cond, true_val, false_val: np.where(cond, true_val, false_val),
        "Conditional: @if_else(condition, true_value, false_value)"
    )
