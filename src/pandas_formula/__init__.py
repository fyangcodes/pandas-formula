"""
pandas-formula: A formula engine for pandas DataFrames.

Example:
    >>> from pandas_formula import FormulaEngine
    >>> import pandas as pd
    >>>
    >>> df = pd.DataFrame({'price': [100, 200], 'qty': [2, 3]})
    >>> engine = FormulaEngine()
    >>> result = engine.apply(df, {'total': '@mul(price, qty)'})
"""

from .engine import FormulaEngine
from .functions import FunctionRegistry, create_default_registry

__version__ = "0.1.0"

__all__ = [
    "FormulaEngine",
    "FunctionRegistry",
    "create_default_registry",
    "__version__",
]
