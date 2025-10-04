import asyncio

from collections.abc import AsyncIterable, AsyncIterator
from dataclasses import dataclass
from typing import Any, Literal, Self, TypeVar, overload

from aioplus.internal.sentinels import Sentinel


T = TypeVar("T")

T1 = TypeVar("T1")
T2 = TypeVar("T2")
T3 = TypeVar("T3")
T4 = TypeVar("T4")
T5 = TypeVar("T5")
T6 = TypeVar("T6")


@overload
def azip(aiterable: AsyncIterable[T], /, *, strict: bool) -> AsyncIterable[tuple[T]]: ...


@overload
def azip(
    aiterable1: AsyncIterable[T1],
    aiterable2: AsyncIterable[T2],
    /,
    *,
    strict: bool = False,
) -> AsyncIterable[tuple[T1, T2]]: ...


@overload
def azip(
    aiterable1: AsyncIterable[T1],
    aiterable2: AsyncIterable[T2],
    aiterable3: AsyncIterable[T3],
    /,
    *,
    strict: bool = False,
) -> AsyncIterable[tuple[T1, T2, T3]]: ...


@overload
def azip(
    aiterable1: AsyncIterable[T1],
    aiterable2: AsyncIterable[T2],
    aiterable3: AsyncIterable[T3],
    aiterable4: AsyncIterable[T4],
    /,
    *,
    strict: bool = False,
) -> AsyncIterable[tuple[T1, T2, T3, T4]]: ...


@overload
def azip(
    aiterable1: AsyncIterable[T1],
    aiterable2: AsyncIterable[T2],
    aiterable3: AsyncIterable[T3],
    aiterable4: AsyncIterable[T4],
    aiterable5: AsyncIterable[T5],
    /,
    *,
    strict: bool = False,
) -> AsyncIterable[tuple[T1, T2, T3, T4, T5]]: ...


@overload
def azip(
    aiterable1: AsyncIterable[T1],
    aiterable2: AsyncIterable[T2],
    aiterable3: AsyncIterable[T3],
    aiterable4: AsyncIterable[T4],
    aiterable5: AsyncIterable[T5],
    aiterable6: AsyncIterable[T6],
    /,
    *,
    strict: bool = False,
) -> AsyncIterable[tuple[T1, T2, T3, T4, T5, T6]]: ...


@overload
def azip(*aiterables: AsyncIterable[T], strict: bool = False) -> AsyncIterable[tuple[T, ...]]: ...


def azip(*aiterables: AsyncIterable[Any], strict: bool = False) -> AsyncIterable[tuple[Any, ...]]:
    """Iterate over several iterables in parallel.

    Parameters
    ----------
    *aiterables : AsyncIterable[T]
        Asynchronous iterables.

    strict : bool, default=False
        If ``True``, raise ``ValueError`` when lengths of ``*aiterables`` differ.

    Returns
    -------
    AsyncIterator[tuple[T, ...]]
        An asynchronous iterable.

    Examples
    --------
    >>> xs = arange(42)
    >>> ys = arange(4, 23)
    >>> [(x, y) async for x, y in azip(xs, ys)]
    [(0, 4), (1, 5), (2, 6), ..., (18, 22)]
    """
    for aiterable in aiterables:
        if not isinstance(aiterable, AsyncIterable):
            detail = "'*aiterables' must be 'AsyncIterable'"
            raise TypeError(detail)

    if not isinstance(strict, bool):
        detail = "'strict' must be 'bool'"
        raise TypeError(detail)

    return AzipIterable(aiterables, strict)


@dataclass
class AzipIterable(AsyncIterable[tuple[T, ...]]):
    """An asynchronous iterable."""

    aiterables: tuple[AsyncIterable[T], ...]
    strict: bool

    def __aiter__(self) -> AsyncIterator[tuple[T, ...]]:
        """Return an asynchronous iterator."""
        aiterators = [aiter(aiterable) for aiterable in self.aiterables]
        return AzipIterator(aiterators, self.strict)


@dataclass
class AzipIterator(AsyncIterator[tuple[T, ...]]):
    """An asynchronous iterator."""

    aiterators: list[AsyncIterator[T]]
    strict: bool

    def __post_init__(self) -> None:
        """Initialize the object."""
        self._finished_flg: bool = False

    def __aiter__(self) -> Self:
        """Return an asynchronous iterator."""
        return self

    async def __anext__(self) -> tuple[T, ...]:
        """Return the next value."""
        if self._finished_flg:
            raise StopAsyncIteration

        coroutines = [self._next_or_sentinel(aiterator) for aiterator in self.aiterators]
        maybes = await asyncio.gather(*coroutines)

        values: list[T] = []
        exceptions: list[Exception] = []

        for maybe_value, maybe_exception in maybes:
            if maybe_value is not Sentinel.EMPTY:
                values.append(maybe_value)
            elif maybe_exception is not Sentinel.UNSET:
                exceptions.append(maybe_exception)

        if exceptions:
            self._finished_flg = True
            detail = "azip(): exception(-s) occurred"
            raise ExceptionGroup(detail, exceptions)

        if not values:
            self._finished_flg = True
            raise StopAsyncIteration

        if self.strict and len(values) < len(maybes):
            self._finished_flg = True
            detail = "azip(): len(aiterable) differ"
            raise ValueError(detail)

        if len(values) < len(maybes):
            self._finished_flg = True
            raise StopAsyncIteration

        return tuple(values)

    async def _next_or_sentinel(
        self,
        aiterator: AsyncIterator[T],
    ) -> tuple[T | Literal[Sentinel.EMPTY], Exception | Literal[Sentinel.UNSET]]:
        """Return the next value or a sentinel."""
        try:
            value = await anext(aiterator)

        except StopAsyncIteration:
            return (Sentinel.EMPTY, Sentinel.UNSET)

        except Exception as exception:
            return (Sentinel.EMPTY, exception)

        return (value, Sentinel.UNSET)
