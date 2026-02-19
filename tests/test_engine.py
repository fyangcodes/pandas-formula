"""Tests for FormulaEngine."""

import numpy as np
import pandas as pd
import pytest

from pandas_formula import FormulaEngine


@pytest.fixture
def sample_df():
    return pd.DataFrame(
        {
            "a": [1, 2, 3],
            "b": [4, 5, 6],
            "c": [7, 8, 9],
            "name": ["alice", "bob", "charlie"],
            "price": [100.0, 200.0, None],
        }
    )


@pytest.fixture
def engine():
    return FormulaEngine()


class TestArithmetic:
    def test_add(self, engine, sample_df):
        result = engine.apply(sample_df, {"result": "@add(a, b)"})
        assert result["result"].tolist() == [5, 7, 9]

    def test_sub(self, engine, sample_df):
        result = engine.apply(sample_df, {"result": "@sub(b, a)"})
        assert result["result"].tolist() == [3, 3, 3]

    def test_mul(self, engine, sample_df):
        result = engine.apply(sample_df, {"result": "@mul(a, b)"})
        assert result["result"].tolist() == [4, 10, 18]

    def test_div(self, engine, sample_df):
        result = engine.apply(sample_df, {"result": "@div(b, a)"})
        assert result["result"].tolist() == [4.0, 2.5, 2.0]

    def test_nested(self, engine, sample_df):
        result = engine.apply(sample_df, {"result": "@add(@mul(a, 2), b)"})
        assert result["result"].tolist() == [6, 9, 12]


class TestComparison:
    def test_gt(self, engine, sample_df):
        result = engine.apply(sample_df, {"result": "@gt(b, 4)"})
        assert result["result"].tolist() == [False, True, True]

    def test_eq(self, engine, sample_df):
        result = engine.apply(sample_df, {"result": "@eq(a, 2)"})
        assert result["result"].tolist() == [False, True, False]


class TestLogical:
    def test_if_else(self, engine, sample_df):
        result = engine.apply(sample_df, {"result": "@if_else(@gt(a, 1), 'yes', 'no')"})
        assert result["result"].tolist() == ["no", "yes", "yes"]


class TestString:
    def test_upper(self, engine, sample_df):
        result = engine.apply(sample_df, {"result": "@upper(name)"})
        assert result["result"].tolist() == ["ALICE", "BOB", "CHARLIE"]

    def test_lower(self, engine, sample_df):
        result = engine.apply(sample_df, {"result": "@lower(name)"})
        assert result["result"].tolist() == ["alice", "bob", "charlie"]


class TestNull:
    def test_coalesce(self, engine, sample_df):
        result = engine.apply(sample_df, {"result": "@coalesce(price, 0)"})
        assert result["result"].tolist() == [100.0, 200.0, 0.0]

    def test_isnull(self, engine, sample_df):
        result = engine.apply(sample_df, {"result": "@isnull(price)"})
        assert result["result"].tolist() == [False, False, True]


class TestCustomFunction:
    def test_register(self, engine, sample_df):
        engine.register("triple", lambda x: x * 3)
        result = engine.apply(sample_df, {"result": "@triple(a)"})
        assert result["result"].tolist() == [3, 6, 9]

    def test_multi_arg(self, engine, sample_df):
        engine.register("weighted", lambda x, y, w: x * w + y * (1 - w))
        result = engine.apply(sample_df, {"result": "@weighted(a, b, 0.5)"})
        assert result["result"].tolist() == [2.5, 3.5, 4.5]


class TestRegisterBatch:
    def test_batch_with_functions(self, engine, sample_df):
        engine.register_batch({
            "triple": lambda x: x * 3,
            "double": lambda x: x * 2,
        })
        result = engine.apply(sample_df, {
            "r1": "@triple(a)",
            "r2": "@double(a)",
        })
        assert result["r1"].tolist() == [3, 6, 9]
        assert result["r2"].tolist() == [2, 4, 6]

    def test_batch_with_doc_tuples(self, engine, sample_df):
        engine.register_batch({
            "triple": (lambda x: x * 3, "Multiply by 3"),
        })
        result = engine.apply(sample_df, {"result": "@triple(a)"})
        assert result["result"].tolist() == [3, 6, 9]
        assert "triple" in engine.list_functions()

    def test_batch_returns_self(self, engine):
        ret = engine.register_batch({"noop": lambda x: x})
        assert ret is engine

    def test_batch_then_chain(self, engine, sample_df):
        engine.register_batch({
            "double": lambda x: x * 2,
        }).register("triple", lambda x: x * 3)
        result = engine.apply(sample_df, {
            "r1": "@double(a)",
            "r2": "@triple(a)",
        })
        assert result["r1"].tolist() == [2, 4, 6]
        assert result["r2"].tolist() == [3, 6, 9]

    def test_batch_empty(self, engine):
        ret = engine.register_batch({})
        assert ret is engine


class TestChaining:
    def test_formula_chaining(self, engine, sample_df):
        result = engine.apply(
            sample_df,
            {
                "step1": "@mul(a, 2)",
                "step2": "@add(step1, b)",
            },
        )
        assert result["step2"].tolist() == [6, 9, 12]


class TestValidation:
    def test_validate_success(self, engine, sample_df):
        errors = engine.validate(sample_df, {"result": "@add(a, b)"})
        assert errors == []

    def test_validate_failure(self, engine, sample_df):
        errors = engine.validate(sample_df, {"result": "@add(a, nonexistent)"})
        assert len(errors) == 1
        assert "result" in errors[0]


class TestExtractReferences:
    def test_single_function_single_arg(self, engine):
        assert engine.extract_references("@my_func(argument)") == {"argument"}

    def test_function_with_kwarg(self, engine):
        assert engine.extract_references("@clip(value, lower=274)") == {"value"}

    def test_function_with_numeric_literal(self, engine):
        assert engine.extract_references("@mul(price, 0.93)") == {"price"}

    def test_nested_function(self, engine):
        assert engine.extract_references("@div(@clip(score, lower=0), 1e6)") == {
            "score"
        }

    def test_multiple_args(self, engine):
        refs = engine.extract_references(
            "@myfunc1(arg1, arg2)"
        )
        assert refs == {"arg1", "arg2"}

    def test_string_literals_excluded(self, engine):
        assert engine.extract_references("@if_else(@gt(score, 70), 'pass', 'fail')") == {
            "score"
        }

    def test_double_quoted_string_excluded(self, engine):
        assert engine.extract_references('@if_else(@gt(score, 70), "pass", "fail")') == {
            "score"
        }

    def test_bare_column_name(self, engine):
        assert engine.extract_references("raw_column") == {"raw_column"}

    def test_numeric_zero(self, engine):
        assert engine.extract_references("0") == set()

    def test_numeric_integer(self, engine):
        assert engine.extract_references("101325") == set()

    def test_bare_identifier(self, engine):
        assert engine.extract_references("timestamps") == {"timestamps"}

    def test_batch(self, engine):
        refs = engine.extract_references_batch(
            {
                "myfunc1": "@myfunc1(arg1)",
                "myfunc2": "@myfunc2(arg2)",
            }
        )
        assert refs == {"arg1", "arg2"}


class TestFromDict:
    def test_from_dict(self, sample_df):
        config = {
            "columns": {
                "sum": "@add(a, b)",
                "product": "@mul(a, b)",
            }
        }
        engine = FormulaEngine.from_dict(config)
        result = engine.apply(sample_df)
        assert result["sum"].tolist() == [5, 7, 9]
        assert result["product"].tolist() == [4, 10, 18]
