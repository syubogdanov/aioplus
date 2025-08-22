from collections.abc import AsyncIterable, Callable, Iterable
from concurrent.futures import Executor
from typing import Literal, LiteralString, ParamSpec, SupportsIndex, TypeVar, overload


P = ParamSpec("P")
R = TypeVar("R")

T1 = TypeVar("T1")
T2 = TypeVar("T2")


def be_int(obj: SupportsIndex | None, /, *, variable_name: LiteralString) -> int:
    """Cast `SupportsIndex` to `int`."""
    if not isinstance(obj, SupportsIndex):
        detail = f"'{variable_name}' must be 'SupportsIndex'"
        raise TypeError(detail)

    obj = obj.__index__()

    if not isinstance(obj, int):
        detail = f"'{variable_name}.__index__()' must be 'int'"
        raise TypeError(detail)

    return obj


def be_positive_int(obj: SupportsIndex | None, /, *, variable_name: LiteralString) -> int:
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


@overload
def be_callable(obj: Callable[P, R], /, *, variable_name: LiteralString) -> Callable[P, R]: ...


@overload
def be_callable(
    obj: Callable[P, R] | None,
    /,
    *,
    variable_name: LiteralString,
    optional: Literal[True],
) -> Callable[P, R] | None: ...


def be_callable(
    obj: Callable[P, R] | None,
    /,
    *,
    variable_name: LiteralString,
    optional: bool = False,
) -> Callable[P, R] | None:
    """Cast `object` to `Callable`."""
    if optional and obj is None:
        return None

    if not callable(obj):
        detail = f"'{variable_name}' must be callable"
        raise TypeError(detail)

    return obj


@overload
def be_executor(obj: Executor, /, *, variable_name: LiteralString) -> Executor: ...


@overload
def be_executor(
    obj: Executor | None,
    /,
    *,
    variable_name: LiteralString,
    optional: Literal[True],
) -> Executor | None: ...


def be_executor(
    obj: Executor | None,
    /,
    *,
    variable_name: LiteralString,
    optional: bool = False,
) -> Executor | None:
    """Cast `object` to `Executor`."""
    if optional and obj is None:
        return None

    if not isinstance(obj, Executor):
        detail = f"'{variable_name}' must be 'Executor'"
        raise TypeError(detail)

    return obj


def be_bool(obj: bool, /, *, variable_name: LiteralString) -> bool:  # noqa: FBT001
    """Cast `object` to `bool`."""
    if not isinstance(obj, bool):
        detail = f"'{variable_name}' must be 'bool'"
        raise TypeError(detail)

    return obj


def be_pair(obj: tuple[T1, T2], /, *, variable_name: LiteralString) -> tuple[T1, T2]:
    """Cast `object` to two-element tuple."""
    if not isinstance(obj, tuple):
        detail = f"'{variable_name}' must be 'tuple'"
        raise TypeError(detail)

    if len(obj) != 2:
        detail = f"'len({variable_name})' must be '2'"
        raise ValueError(detail)

    return obj


def be_iterable(
    obj: Iterable[T1],
    /,
    *,
    variable_name: LiteralString,
) -> Iterable[T1]:
    """Cast `object` to `Iterable`."""
    if not isinstance(obj, Iterable):
        detail = f"'{variable_name}' must be 'Iterable'"
        raise TypeError(detail)

    return obj
