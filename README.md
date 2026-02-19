# pandas-formula

A formula engine for pandas DataFrames.

Define column calculations using a simple `@function(args)` syntax and apply them to your DataFrames.

## Installation

```bash
# From GitHub
pip install git+https://github.com/fyangcodes/pandas-formula.git

# For development
git clone https://github.com/fyangcodes/pandas-formula.git
cd pandas-formula
pip install -e ".[dev]"
```

## Quick Start

```python
from pandas_formula import FormulaEngine
import pandas as pd

# Create a DataFrame
df = pd.DataFrame({
    'price': [100, 200, 150],
    'quantity': [2, 3, 4],
    'cost': [80, 150, 100]
})

# Create engine and apply formulas
engine = FormulaEngine()
result = engine.apply(df, {
    'total': '@mul(price, quantity)',
    'profit': '@sub(total, cost)',
    'margin': '@div(profit, total)',
})

print(result)
```

## Custom Functions

Register your own functions:

```python
import numpy as np

engine = FormulaEngine()

# Simple function
engine.register('margin', lambda revenue, cost: (revenue - cost) / revenue)

# Multi-level conditional
engine.register('grade', lambda score: np.where(
    score >= 90, 'A',
    np.where(score >= 80, 'B',
    np.where(score >= 70, 'C', 'F'))
))

# Use in formulas
result = engine.apply(df, {
    'profit_margin': '@margin(revenue, cost)',
    'letter_grade': '@grade(score)',
})
```

## Built-in Functions

### Arithmetic
| Function | Example | Description |
|----------|---------|-------------|
| `@add` | `@add(a, b)` | Addition |
| `@sub` | `@sub(a, b)` | Subtraction |
| `@mul` | `@mul(a, b)` | Multiplication |
| `@div` | `@div(a, b)` | Division |
| `@mod` | `@mod(a, b)` | Modulo |
| `@pow` | `@pow(a, 2)` | Power |
| `@abs` | `@abs(a)` | Absolute value |

### Comparison
| Function | Example | Description |
|----------|---------|-------------|
| `@eq` | `@eq(a, b)` | Equal |
| `@ne` | `@ne(a, b)` | Not equal |
| `@gt` | `@gt(a, b)` | Greater than |
| `@gte` | `@gte(a, b)` | Greater or equal |
| `@lt` | `@lt(a, b)` | Less than |
| `@lte` | `@lte(a, b)` | Less or equal |

### Logical
| Function | Example | Description |
|----------|---------|-------------|
| `@and_` | `@and_(a, b)` | Logical AND |
| `@or_` | `@or_(a, b)` | Logical OR |
| `@not_` | `@not_(a)` | Logical NOT |
| `@if_else` | `@if_else(cond, true_val, false_val)` | Conditional |

### String
| Function | Example | Description |
|----------|---------|-------------|
| `@upper` | `@upper(name)` | Uppercase |
| `@lower` | `@lower(name)` | Lowercase |
| `@strip` | `@strip(name)` | Strip whitespace |
| `@concat` | `@concat(a, b)` | Concatenate |
| `@contains` | `@contains(a, 'pattern')` | Contains pattern |

### Null Handling
| Function | Example | Description |
|----------|---------|-------------|
| `@isnull` | `@isnull(a)` | Check null |
| `@notnull` | `@notnull(a)` | Check not null |
| `@coalesce` | `@coalesce(a, b)` | First non-null |
| `@fillna` | `@fillna(a, 0)` | Fill nulls |

### Math
| Function | Example | Description |
|----------|---------|-------------|
| `@round` | `@round(a, 2)` | Round |
| `@ceil` | `@ceil(a)` | Ceiling |
| `@floor` | `@floor(a)` | Floor |
| `@sqrt` | `@sqrt(a)` | Square root |
| `@log` | `@log(a)` | Natural log |
| `@clip` | `@clip(a, 0, 100)` | Clip values |

### Aggregation
| Function | Example | Description |
|----------|---------|-------------|
| `@sum` | `@sum(a)` | Sum |
| `@mean` | `@mean(a)` | Mean |
| `@min` | `@min(a)` | Minimum |
| `@max` | `@max(a)` | Maximum |
| `@std` | `@std(a)` | Standard deviation |
| `@pct_of_total` | `@pct_of_total(a)` | Percentage of total |

## Batch Registration

Register multiple custom functions at once with `register_batch()`. Values can be a plain function or a `(function, doc)` tuple:

```python
engine = FormulaEngine()
engine.register_batch({
    'margin': (lambda r, c: (r - c) / r, 'Profit margin ratio'),
    'roi': lambda r, c: (r - c) / c,
})
```

## Method Chaining

All registration methods return `self`, so you can chain freely:

```python
engine = (
    FormulaEngine()
    .register_batch({
        'margin': (lambda r, c: (r - c) / r, 'Profit margin ratio'),
        'roi': lambda r, c: (r - c) / c,
    })
    .register('fmt_pct', lambda x: (x * 100).round(1))
    .add_formula('profit', '@sub(revenue, cost)')
    .add_formula('margin_pct', '@fmt_pct(@margin(revenue, cost))')
    .add_formula('roi_pct', '@fmt_pct(@roi(revenue, cost))')
)

result = engine.apply(df)
```

## Validation

```python
errors = engine.validate(df, formulas)
if errors:
    for err in errors:
        print(f"Error: {err}")
```

## Extract References

Statically analyze formulas to find which column names they reference, without executing anything:

```python
engine = FormulaEngine()

# Single formula
engine.extract_references('@mul(price, quantity)')
# {'price', 'quantity'}

engine.extract_references('@clip(value, lower=0)')
# {'value'}  — keyword args and numeric literals are excluded

engine.extract_references('@if_else(@gt(score, 70), "pass", "fail")')
# {'score'}  — string literals and function names are excluded

# Batch extraction from a dict of formulas
engine.extract_references_batch({
    'total': '@mul(price, quantity)',
    'status': '@if_else(@gt(score, 70), "pass", "fail")',
})
# {'price', 'quantity', 'score'}
```

## Export

```python
# Export to dict
config = engine.to_dict()
```

## How It Works

This library leverages `pandas.DataFrame.eval()` with the `engine='python'` option. Functions are registered as local variables and invoked using the `@` syntax that `eval()` supports for local variable references.

```python
# Under the hood:
df.eval('total = @mul(price, quantity)', local_dict={'mul': lambda a, b: a * b}, engine='python')
```

## License

MIT
