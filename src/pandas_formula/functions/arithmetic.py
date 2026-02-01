"""Arithmetic functions."""

import numpy as np

from .registry import FunctionRegistry


def register_arithmetic_functions(registry: FunctionRegistry) -> None:
    """Register arithmetic functions."""

    registry.register("add", lambda a, b: a + b, "Add two values: @add(a, b)")
    registry.register("sub", lambda a, b: a - b, "Subtract: @sub(a, b)")
    registry.register("mul", lambda a, b: a * b, "Multiply: @mul(a, b)")
    registry.register("div", lambda a, b: a / b, "Divide: @div(a, b)")
    registry.register("floordiv", lambda a, b: a // b, "Floor divide: @floordiv(a, b)")
    registry.register("mod", lambda a, b: a % b, "Modulo: @mod(a, b)")
    registry.register("pow", lambda a, b: a ** b, "Power: @pow(a, b)")
    registry.register("neg", lambda a: -a, "Negate: @neg(a)")
    registry.register("abs", lambda a: np.abs(a), "Absolute value: @abs(a)")
