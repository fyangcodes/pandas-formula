"""Aggregation functions."""

from .registry import FunctionRegistry


def register_aggregation_functions(registry: FunctionRegistry) -> None:
    """Register aggregation functions.

    Note: These return scalars which broadcast back to the column length.
    """

    registry.register("sum", lambda a: a.sum(), "Sum: @sum(a)")
    registry.register("mean", lambda a: a.mean(), "Mean: @mean(a)")
    registry.register("median", lambda a: a.median(), "Median: @median(a)")
    registry.register("min", lambda a: a.min(), "Minimum: @min(a)")
    registry.register("max", lambda a: a.max(), "Maximum: @max(a)")
    registry.register("std", lambda a: a.std(), "Standard deviation: @std(a)")
    registry.register("var", lambda a: a.var(), "Variance: @var(a)")
    registry.register("count", lambda a: a.count(), "Count non-null: @count(a)")
    registry.register(
        "pct_of_total",
        lambda a: a / a.sum() * 100,
        "Percentage of total: @pct_of_total(a)"
    )
    registry.register(
        "normalize",
        lambda a: (a - a.min()) / (a.max() - a.min()),
        "Normalize 0-1: @normalize(a)"
    )
    registry.register(
        "zscore",
        lambda a: (a - a.mean()) / a.std(),
        "Z-score: @zscore(a)"
    )
