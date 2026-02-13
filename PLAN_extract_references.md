# Plan: Add extract_references() to FormulaEngine

## Context

Statically analyze formula strings to extract column name references. This method belongs in FormulaEngine since it understands the `@function(args)` syntax.

## File to modify

`src/pandas_formula/engine.py`

## Implementation

Add module-level regex patterns and two instance methods:

```python
import re

# Module-level patterns
_FUNC_PATTERN = re.compile(r'@(\w+)')
_KWARG_PATTERN = re.compile(r'\b(\w+)\s*=')
_NUMERIC_PATTERN = re.compile(r'^-?\d+\.?\d*$')
_SCI_NOTATION = re.compile(r'\d+\.?\d*e[+-]?\d+', re.IGNORECASE)
_IDENTIFIER_PATTERN = re.compile(r'[A-Za-z_][\w.\[\]]*')
```

### `extract_references(formula) -> set[str]`

Statically analyzes a formula string and returns all referenced column names, excluding `@function` names, numeric literals, and keyword args.

```python
def extract_references(self, formula: str) -> set[str]:
    """Extract column name references from a formula string.

    Statically analyzes without executing. Returns identifiers that are
    not registered functions, numeric literals, or keyword arguments.

    Args:
        formula: Formula string (e.g. '@my_func(argument)')

    Returns:
        Set of referenced column names (e.g. {'argument'})

    Examples:
        >>> engine.extract_references('@scale(temperature)')
        {'temperature'}

        >>> engine.extract_references('@clip(value, lower=274)')
        {'value'}

        >>> engine.extract_references('@mul(price, 0.93)')
        {'price'}

        >>> engine.extract_references('0')
        set()
    """
    func_names = set(_FUNC_PATTERN.findall(formula))
    kwarg_names = set(_KWARG_PATTERN.findall(formula))
    # Remove scientific notation before extracting identifiers
    cleaned = _SCI_NOTATION.sub('', formula)
    all_ids = set(_IDENTIFIER_PATTERN.findall(cleaned))

    return {
        name for name in all_ids
        if name not in func_names
        and name not in kwarg_names
        and not _NUMERIC_PATTERN.match(name)
    }
```

### `extract_references_batch(formulas) -> set[str]`

Batch version for a dict of formulas.

```python
def extract_references_batch(self, formulas: dict[str, str]) -> set[str]:
    """Extract all column references from a dict of formulas.

    Args:
        formulas: Dict of target_column -> formula_string

    Returns:
        Union of all referenced column names across all formulas

    Examples:
        >>> engine.extract_references_batch({
        ...     'total': '@mul(price, quantity)',
        ...     'label': '@upper(name)',
        ... })
        {'price', 'quantity', 'name'}
    """
    refs = set()
    for formula in formulas.values():
        refs |= self.extract_references(formula)
    return refs
```

## Expected behavior

| Formula | Returns |
|---------|---------|
| `@scale(temperature)` | `{temperature}` |
| `@clip(value, lower=274)` | `{value}` |
| `@mul(price, 0.93)` | `{price}` |
| `@div(@clip(score, lower=0), 1e6)` | `{score}` |
| `@weighted_avg(col_a, col_b)` | `{col_a, col_b}` |
| `raw_column` | `{raw_column}` |
| `0` | `{}` |
| `101325` | `{}` |
| `timestamps` | `{timestamps}` |

Note: `timestamps` is returned as-is — the caller decides whether it's a keyword or column name.

## Verification

```bash
python -c "
from pandas_formula import FormulaEngine
e = FormulaEngine()
assert e.extract_references('@scale(temperature)') == {'temperature'}
assert e.extract_references('@clip(value, lower=274)') == {'value'}
assert e.extract_references('@mul(price, 0.93)') == {'price'}
assert e.extract_references('0') == set()
assert e.extract_references('raw_column') == {'raw_column'}
print('All assertions passed')
"
```
