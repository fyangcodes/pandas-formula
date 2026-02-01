"""
Built-in functions for the pandas formula engine.
"""

from .registry import FunctionRegistry
from .arithmetic import register_arithmetic_functions
from .comparison import register_comparison_functions
from .logical import register_logical_functions
from .string import register_string_functions
from .null import register_null_functions
from .math import register_math_functions
from .aggregation import register_aggregation_functions


def create_default_registry() -> FunctionRegistry:
    """Create a registry with all default functions registered."""
    registry = FunctionRegistry()
    register_arithmetic_functions(registry)
    register_comparison_functions(registry)
    register_logical_functions(registry)
    register_string_functions(registry)
    register_null_functions(registry)
    register_math_functions(registry)
    register_aggregation_functions(registry)
    return registry


__all__ = [
    "FunctionRegistry",
    "create_default_registry",
]
