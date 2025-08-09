from typing import LiteralString, SupportsIndex


def to_int(obj: SupportsIndex, /, *, variable_name: LiteralString) -> int:
    """Cast `SupportsIndex` to `int`."""
    if not isinstance(obj, SupportsIndex):
        detail = f"'{variable_name}' must be 'SupportsIndex'"
        raise TypeError(detail)

    obj = obj.__index__()

    if not isinstance(obj, int):
        detail = f"'{variable_name}.__index__()' must be 'int'"
        raise TypeError(detail)

    return obj


def to_positive_int(obj: SupportsIndex, /, *, variable_name: LiteralString) -> int:
    """Cast `SupportsIndex` to `int`.

    Notes
    -----
    * Raises `ValueError` if `obj.__index__()` is negative or zero.
    """
    obj = to_int(obj, variable_name=variable_name)

    if obj <= 0:
        detail = f"'{variable_name}' must be positive"
        raise ValueError(detail)

    return obj


def to_non_negative_int(obj: SupportsIndex, /, *, variable_name: LiteralString) -> int:
    """Cast `SupportsIndex` to `int`.

    Notes
    -----
    * Raises `ValueError` if `obj.__index__()` is negative.
    """
    obj = to_int(obj, variable_name=variable_name)

    if obj < 0:
        detail = f"'{variable_name}' must be non-negative"
        raise ValueError(detail)

    return obj
