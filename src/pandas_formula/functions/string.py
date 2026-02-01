"""String functions."""

from .registry import FunctionRegistry


def register_string_functions(registry: FunctionRegistry) -> None:
    """Register string functions."""

    registry.register("upper", lambda a: a.str.upper(), "Uppercase: @upper(a)")
    registry.register("lower", lambda a: a.str.lower(), "Lowercase: @lower(a)")
    registry.register("strip", lambda a: a.str.strip(), "Strip whitespace: @strip(a)")
    registry.register("lstrip", lambda a: a.str.lstrip(), "Left strip: @lstrip(a)")
    registry.register("rstrip", lambda a: a.str.rstrip(), "Right strip: @rstrip(a)")
    registry.register(
        "concat",
        lambda a, b: a.astype(str) + b.astype(str),
        "Concatenate: @concat(a, b)"
    )
    registry.register(
        "concat3",
        lambda a, b, c: a.astype(str) + b.astype(str) + c.astype(str),
        "Concatenate 3: @concat3(a, b, c)"
    )
    registry.register(
        "concat_sep",
        lambda a, b, sep: a.str.cat(b, sep=sep),
        "Concatenate with separator: @concat_sep(a, b, ' ')"
    )
    registry.register("str_len", lambda a: a.str.len(), "String length: @str_len(a)")
    registry.register(
        "contains",
        lambda a, pattern: a.str.contains(pattern, na=False),
        "Contains pattern: @contains(a, 'pattern')"
    )
    registry.register(
        "startswith",
        lambda a, prefix: a.str.startswith(prefix, na=False),
        "Starts with: @startswith(a, 'prefix')"
    )
    registry.register(
        "endswith",
        lambda a, suffix: a.str.endswith(suffix, na=False),
        "Ends with: @endswith(a, 'suffix')"
    )
    registry.register(
        "replace",
        lambda a, old, new: a.str.replace(old, new, regex=False),
        "Replace: @replace(a, 'old', 'new')"
    )
    registry.register(
        "slice",
        lambda a, start, end: a.str.slice(start, end),
        "Slice string: @slice(a, 0, 5)"
    )
