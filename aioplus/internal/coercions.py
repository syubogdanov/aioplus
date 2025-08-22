from collections.abc import AsyncIterable, Callable, Iterable
from concurrent.futures import Executor
from typing import LiteralString, ParamSpec, SupportsIndex, TypeVar


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
    """Cast `SupportsIndex` to `int`.

    Notes
    -----
    * Raises `ValueError` if `obj.__index__()` is negative or zero.
    """
    obj = be_int(obj, variable_name=variable_name)

    if obj <= 0:
        detail = f"'{variable_name}' must be positive"
        raise ValueError(detail)

    return obj


def be_non_negative_int(obj: SupportsIndex, /, *, variable_name: LiteralString) -> int:
    """Cast `SupportsIndex` to `int`.

    Notes
    -----
    * Raises `ValueError` if `obj.__index__()` is negative.
    """
    obj = be_int(obj, variable_name=variable_name)

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
    """Cast `object` to `AsyncIterable`.

    Notes
    -----
    * Raises `TypeError` if `obj` is not `AsyncIterable`.
    """
    if not isinstance(obj, AsyncIterable):
        detail = f"'{variable_name}' must be 'AsyncIterable'"
        raise TypeError(detail)

    return obj


def be_callable(obj: Callable[P, R], /, *, variable_name: LiteralString) -> Callable[P, R]:
    """Cast `object` to `Callable`.

    Notes
    -----
    * Raises `TypeError` if `obj` is not `Callable`.
    """
    if not callable(obj):
        detail = f"'{variable_name}' must be callable"
        raise TypeError(detail)

    return obj


def be_executor(obj: Executor, /, *, variable_name: LiteralString) -> Executor:
    """Cast `object` to `Executor`.

    Notes
    -----
    * Raises `TypeError` if `obj` is not `Executor`.
    """
    if not isinstance(obj, Executor):
        detail = f"'{variable_name}' must be 'Executor'"
        raise TypeError(detail)

    return obj


def be_bool(obj: bool, /, *, variable_name: LiteralString) -> bool:  # noqa: FBT001
    """Cast `object` to `bool`.

    Notes
    -----
    * Raises `TypeError` if `obj` is not `bool`.
    """
    if not isinstance(obj, bool):
        detail = f"'{variable_name}' must be 'bool'"
        raise TypeError(detail)

    return obj


def be_pair(obj: tuple[T1, T2], /, *, variable_name: LiteralString) -> tuple[T1, T2]:
    """Cast `object` to two-element tuple.

    Notes
    -----
    * Raises `TypeError` if `obj` is not `tuple`;
    * Raises `ValueError` if `len(obj) != 2`.
    """
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
    """Cast `object` to `Iterable`.

    Notes
    -----
    * Raises `TypeError` if `obj` is not `Iterable`.
    """
    if not isinstance(obj, Iterable):
        detail = f"'{variable_name}' must be 'Iterable'"
        raise TypeError(detail)

    return obj
