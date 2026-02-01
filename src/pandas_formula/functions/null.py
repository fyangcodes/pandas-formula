"""Null handling functions."""

from .registry import FunctionRegistry


def register_null_functions(registry: FunctionRegistry) -> None:
    """Register null handling functions."""

    registry.register("isnull", lambda a: a.isnull(), "Check null: @isnull(a)")
    registry.register("notnull", lambda a: a.notnull(), "Check not null: @notnull(a)")
    registry.register(
        "coalesce",
        lambda a, b: a.fillna(b),
        "Return first non-null: @coalesce(a, b)"
    )
    registry.register(
        "fillna",
        lambda a, val: a.fillna(val),
        "Fill null with value: @fillna(a, 0)"
    )
    registry.register(
        "dropna",
        lambda a: a.dropna(),
        "Drop null values: @dropna(a)"
    )
