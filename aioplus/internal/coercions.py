from collections.abc import AsyncIterable
from typing import Literal, LiteralString, ParamSpec, SupportsIndex, TypeVar, overload


P = ParamSpec("P")
R = TypeVar("R")

T1 = TypeVar("T1")
T2 = TypeVar("T2")


def be_int(obj: SupportsIndex, /, *, variable_name: LiteralString) -> int:
    """Cast `SupportsIndex` to `int`."""
    if not isinstance(obj, SupportsIndex):
        detail = f"'{variable_name}' must be 'SupportsIndex'"
        raise TypeError(detail)

    obj = obj.__index__()

    if not isinstance(obj, int):
        detail = f"'{variable_name}.__index__()' must be 'int'"
        raise TypeError(detail)

    return obj


def be_positive_int(obj: SupportsIndex, /, *, variable_name: LiteralString) -> int:
    """Cast `SupportsIndex` to `int` [positive]."""
    if not isinstance(obj, SupportsIndex):
        detail = f"'{variable_name}' must be 'SupportsIndex'"
        raise TypeError(detail)

    obj = obj.__index__()

    if not isinstance(obj, int):
        detail = f"'{variable_name}.__index__()' must be 'int'"
        raise TypeError(detail)

    if obj <= 0:
        detail = f"'{variable_name}' must be positive"
        raise ValueError(detail)

    return obj


@overload
def be_non_negative_int(obj: SupportsIndex, /, *, variable_name: LiteralString) -> int: ...


@overload
def be_non_negative_int(
    obj: SupportsIndex | None,
    /,
    *,
    variable_name: LiteralString,
    optional: Literal[True],
) -> int | None: ...


def be_non_negative_int(
    obj: SupportsIndex | None,
    /,
    *,
    variable_name: LiteralString,
    optional: bool = False,
) -> int | None:
    """Cast `SupportsIndex` to `int` [non-negative]."""
    if optional and obj is None:
        return None

    if not isinstance(obj, SupportsIndex):
        detail = f"'{variable_name}' must be 'SupportsIndex'"
        raise TypeError(detail)

    obj = obj.__index__()

    if not isinstance(obj, int):
        detail = f"'{variable_name}.__index__()' must be 'int'"
        raise TypeError(detail)

    if obj < 0:
        detail = f"'{variable_name}' must be non-negative"
        raise ValueError(detail)

    return obj


def be_async_iterable(
    obj: AsyncIterable[T1],
    /,
    *,
    variable_name: LiteralString,
) -> AsyncIterable[T1]:
    """Cast `object` to `AsyncIterable`."""
    if not isinstance(obj, AsyncIterable):
        detail = f"'{variable_name}' must be 'AsyncIterable'"
        raise TypeError(detail)

    return obj


def be_bool(obj: bool, /, *, variable_name: LiteralString) -> bool:  # noqa: FBT001
    """Cast `object` to `bool`."""
    if not isinstance(obj, bool):
        detail = f"'{variable_name}' must be 'bool'"
        raise TypeError(detail)

    return obj
