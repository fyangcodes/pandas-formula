"""Comparison functions."""

from .registry import FunctionRegistry


def register_comparison_functions(registry: FunctionRegistry) -> None:
    """Register comparison functions."""

    registry.register("eq", lambda a, b: a == b, "Equal: @eq(a, b)")
    registry.register("ne", lambda a, b: a != b, "Not equal: @ne(a, b)")
    registry.register("gt", lambda a, b: a > b, "Greater than: @gt(a, b)")
    registry.register("gte", lambda a, b: a >= b, "Greater than or equal: @gte(a, b)")
    registry.register("lt", lambda a, b: a < b, "Less than: @lt(a, b)")
    registry.register("lte", lambda a, b: a <= b, "Less than or equal: @lte(a, b)")
