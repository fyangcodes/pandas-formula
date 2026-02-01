"""Math functions."""

import numpy as np

from .registry import FunctionRegistry


def register_math_functions(registry: FunctionRegistry) -> None:
    """Register math functions."""

    registry.register("round", lambda a, n=0: np.round(a, n), "Round: @round(a, 2)")
    registry.register("ceil", lambda a: np.ceil(a), "Ceiling: @ceil(a)")
    registry.register("floor", lambda a: np.floor(a), "Floor: @floor(a)")
    registry.register("sqrt", lambda a: np.sqrt(a), "Square root: @sqrt(a)")
    registry.register("log", lambda a: np.log(a), "Natural log: @log(a)")
    registry.register("log10", lambda a: np.log10(a), "Log base 10: @log10(a)")
    registry.register("log2", lambda a: np.log2(a), "Log base 2: @log2(a)")
    registry.register("exp", lambda a: np.exp(a), "Exponential: @exp(a)")
    registry.register("sin", lambda a: np.sin(a), "Sine: @sin(a)")
    registry.register("cos", lambda a: np.cos(a), "Cosine: @cos(a)")
    registry.register("tan", lambda a: np.tan(a), "Tangent: @tan(a)")
    registry.register(
        "clip",
        lambda a, lower, upper: np.clip(a, lower, upper),
        "Clip values: @clip(a, 0, 100)"
    )
