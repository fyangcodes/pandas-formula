"""
Formula Engine - Main engine for evaluating formulas on pandas DataFrames.
"""

from __future__ import annotations

from typing import Any, Callable

import pandas as pd

from .functions import FunctionRegistry, create_default_registry


class FormulaEngine:
    """Engine for evaluating formulas on pandas DataFrames.

    Formulas use @ syntax to call registered functions:
        @add(price, quantity)
        @if_else(@gt(total, 100), 'high', 'low')

    Example:
        >>> engine = FormulaEngine()
        >>> df = pd.DataFrame({'price': [100, 200], 'qty': [2, 3]})
        >>> result = engine.apply(df, {'total': '@mul(price, qty)'})
    """

    def __init__(self, include_defaults: bool = True):
        """Initialize the formula engine.

        Args:
            include_defaults: Whether to include default functions (default: True)
        """
        if include_defaults:
            self._registry = create_default_registry()
        else:
            self._registry = FunctionRegistry()

        self._constants: dict[str, Any] = {}
        self._formulas: dict[str, str] = {}

    @property
    def registry(self) -> FunctionRegistry:
        """Access the function registry."""
        return self._registry

    def register(self, name: str, func: Callable, doc: str = "") -> "FormulaEngine":
        """Register a custom function.

        Args:
            name: Function name (called as @name in formulas)
            func: Function implementation
            doc: Optional documentation

        Returns:
            self for method chaining

        Example:
            >>> engine.register('margin', lambda rev, cost: (rev - cost) / rev)
        """
        self._registry.register(name, func, doc)
        return self

    def add_constant(self, name: str, value: Any) -> "FormulaEngine":
        """Add a constant value.

        Constants can be referenced in formulas but are not currently
        supported with df.eval(). Use register() with a lambda instead.

        Args:
            name: Constant name
            value: Constant value

        Returns:
            self for method chaining
        """
        self._constants[name] = value
        # Also register as a function that returns the constant
        self._registry.register(name, lambda: value)
        return self

    def add_formula(self, column: str, formula: str) -> "FormulaEngine":
        """Add a formula for a column.

        Args:
            column: Target column name
            formula: Formula string (e.g., '@add(a, b)')

        Returns:
            self for method chaining
        """
        self._formulas[column] = formula
        return self

    def _eval_formula(
        self, df: pd.DataFrame, column: str, formula: str
    ) -> None:
        """Evaluate a single formula on a DataFrame.

        Args:
            df: DataFrame to evaluate on (modified inplace)
            column: Target column name
            formula: Formula string

        Raises:
            Exception: If formula evaluation fails
        """
        df.eval(
            f"{column} = {formula}",
            local_dict=self._registry.as_dict(),
            engine="python",
            inplace=True,
        )

    def _resolve_formulas(
        self, formulas: dict[str, str] | None
    ) -> dict[str, str]:
        """Resolve formulas, using internal formulas if none provided."""
        return formulas or self._formulas

    def apply(
        self,
        df: pd.DataFrame,
        formulas: dict[str, str] | None = None,
        inplace: bool = False,
    ) -> pd.DataFrame:
        """Apply formulas to a DataFrame.

        Args:
            df: Input DataFrame
            formulas: Dict of column -> formula. If None, uses formulas
                     added via add_formula()
            inplace: If True, modify df directly (default: False)

        Returns:
            DataFrame with calculated columns

        Raises:
            ValueError: If formula evaluation fails
        """
        result = df if inplace else df.copy()

        formulas = self._resolve_formulas(formulas)
        if not formulas:
            return result

        for column, formula in formulas.items():
            try:
                self._eval_formula(result, column, formula)
            except Exception as e:
                raise ValueError(
                    f"Failed to evaluate formula for '{column}': {formula}\n"
                    f"Error: {e}"
                ) from e

        return result

    def validate(
        self, df: pd.DataFrame, formulas: dict[str, str] | None = None
    ) -> list[str]:
        """Validate formulas against a DataFrame without executing.

        Args:
            df: DataFrame to validate against
            formulas: Formulas to validate (or use internal formulas)

        Returns:
            List of error messages (empty if valid)
        """
        sample = df.head(1).copy()
        
        formulas = self._resolve_formulas(formulas)
        errors = []

        for column, formula in formulas.items():
            try:
                self._eval_formula(sample, column, formula)
            except Exception as e:
                errors.append(f"{column}: {e}")

        return errors

    def list_functions(self) -> list[str]:
        """List all registered functions."""
        return self._registry.list_functions()

    @classmethod
    def from_dict(cls, config: dict, **kwargs) -> "FormulaEngine":
        """Load engine configuration from a dictionary.

        Args:
            config: Configuration dictionary with 'columns' and optional 'constants'
            **kwargs: Additional arguments for FormulaEngine()

        Returns:
            Configured FormulaEngine
        """
        engine = cls(**kwargs)

        # Load constants
        for name, value in config.get("constants", {}).items():
            engine.add_constant(name, value)

        # Load formulas
        columns = config.get("columns", {})
        for column, col_config in columns.items():
            if isinstance(col_config, str):
                formula = col_config
            else:
                formula = col_config.get("formula", "")
                if not col_config.get("enabled", True):
                    continue

            if formula:
                engine.add_formula(column, formula)

        return engine

    def to_dict(self) -> dict:
        """Export configuration to a dictionary."""
        from . import __version__

        return {
            "version": __version__,
            "constants": self._constants.copy(),
            "columns": self._formulas.copy(),
        }
