"""
Pandas Formula Engine Demo

Run after installing the package:
    pip install -e .
    python examples/demo.py
"""
from pprint import pprint

import numpy as np
import pandas as pd

from pandas_formula import FormulaEngine


def demo_common():
    print("=" * 60)
    print("PANDAS FORMULA ENGINE DEMO")
    print("=" * 60)

    # Create sample data
    df = pd.DataFrame(
        {
            "first_name": ["Alice", "Bob", "Charlie", "Diana"],
            "last_name": ["Smith", "Jones", "Brown", "Wilson"],
            "price": [100.0, 200.0, 150.0, None],
            "quantity": [2, 3, 4, 5],
            "cost": [80.0, 150.0, 100.0, 120.0],
            "score": [85, 72, 55, 90],
        }
    )

    print("\n[INPUT DATA]")
    print(df)

    # Initialize engine
    engine = FormulaEngine()

    # Register custom functions
    engine.register(
        "grade",
        lambda s: np.where(
            s >= 90,
            "A",
            np.where(s >= 80, "B", np.where(s >= 70, "C", np.where(s >= 60, "D", "F"))),
        ),
        "Convert score to letter grade",
    )

    engine.register(
        "full_name",
        lambda first, last: first.str.cat(last, sep=" "),
        "Combine first and last name",
    )

    engine.register(
        "profit_margin",
        lambda price, qty, cost: ((price * qty) - cost) / (price * qty),
        "Calculate profit margin",
    )

    # Define formulas
    formulas = {
        # Null handling
        "price_clean": "@coalesce(price, 0)",
        # Basic arithmetic
        "subtotal": "@mul(price_clean, quantity)",
        # Using registered custom function
        "margin": "@profit_margin(price_clean, quantity, cost)",
        # Conditional
        "status": "@if_else(@gt(score, 70), 'pass', 'fail')",
        # Custom grade function
        "grade": "@grade(score)",
        # String operations
        "name": "@full_name(first_name, last_name)",
        "name_upper": "@upper(name)",
        # Math
        "margin_pct": "@round(@mul(margin, 100), 1)",
    }

    print("\n[APPLYING FORMULAS]")
    pprint(formulas)

    result = engine.apply(df, formulas)

    print("\n[OUTPUT]")
    print(result[formulas.keys()].to_string())

    # Validate formulas
    print("\n[VALIDATION]")
    errors = engine.validate(df, formulas)
    if errors:
        print("Errors found:")
        for err in errors:
            print(f"  - {err}")
    else:
        print("All formulas valid!")

    # List available functions
    print("\n[AVAILABLE FUNCTIONS]")
    functions = engine.list_functions()
    print(f"  {len(functions)} functions registered")
    print(f"  Sample: {functions[:10]}...")

    print("\n" + "=" * 60)


def demo_chaining():
    """Demo method chaining API."""
    print("\n" + "=" * 60)
    print("METHOD CHAINING DEMO")
    print("=" * 60)

    df = pd.DataFrame(
        {
            "revenue": [1000, 2000, 1500],
            "cost": [600, 1400, 900],
        }
    )

    # Fluent API
    engine = (
        FormulaEngine()
        .register("margin", lambda r, c: (r - c) / r)
        .add_formula("profit", "@sub(revenue, cost)")
        .add_formula("margin_pct", "@mul(@margin(revenue, cost), 100)")
    )

    result = engine.apply(df)

    print("\n[RESULT]")
    print(result.to_string())


def demo_extract_references():
    """Demo extracting column references from formulas."""
    print("\n" + "=" * 60)
    print("EXTRACT REFERENCES DEMO")
    print("=" * 60)

    engine = FormulaEngine()

    # Single formula
    examples = [
        "@mul(price, quantity)",
        "@clip(value, lower=0)",
        "@div(@add(revenue, bonus), 1e6)",
        "raw_column",
        "3.14",
    ]

    print("\n[SINGLE FORMULA]")
    for formula in examples:
        refs = engine.extract_references(formula)
        print(f"  {formula!r:45s} -> {refs}")

    # Batch extraction
    formulas = {
        "price_clean": "@coalesce(price, 0)",
        "subtotal": "@mul(price_clean, quantity)",
        "status": "@if_else(@gt(score, 70), 'pass', 'fail')",
        "margin_pct": "@round(@mul(margin, 100), 1)",
    }

    print("\n[BATCH EXTRACTION]")
    pprint(formulas)
    all_refs = engine.extract_references_batch(formulas)
    print(f"\n  All referenced columns: {sorted(all_refs)}")


if __name__ == "__main__":
    demo_common()
    demo_chaining()
    demo_extract_references()
