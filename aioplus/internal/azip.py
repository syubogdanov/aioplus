from asyncio import TaskGroup
from collections.abc import AsyncIterable, AsyncIterator
from dataclasses import dataclass
from typing import Any, TypeVar, overload

from aioplus.internal.utils.abc import AioplusIterator


T = TypeVar("T")

T1 = TypeVar("T1")
T2 = TypeVar("T2")
T3 = TypeVar("T3")
T4 = TypeVar("T4")
T5 = TypeVar("T5")
T6 = TypeVar("T6")


@overload
def azip(aiterable: AsyncIterable[T], /, *, strict: bool) -> AsyncIterator[tuple[T]]: ...


@overload
def azip(
    aiterable1: AsyncIterable[T1],
    aiterable2: AsyncIterable[T2],
    /,
    *,
    strict: bool = False,
) -> AsyncIterator[tuple[T1, T2]]: ...


@overload
def azip(
    aiterable1: AsyncIterable[T1],
    aiterable2: AsyncIterable[T2],
    aiterable3: AsyncIterable[T3],
    /,
    *,
    strict: bool = False,
) -> AsyncIterator[tuple[T1, T2, T3]]: ...


@overload
def azip(
    aiterable1: AsyncIterable[T1],
    aiterable2: AsyncIterable[T2],
    aiterable3: AsyncIterable[T3],
    aiterable4: AsyncIterable[T4],
    /,
    *,
    strict: bool = False,
) -> AsyncIterator[tuple[T1, T2, T3, T4]]: ...


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
) -> AsyncIterator[tuple[T1, T2, T3, T4, T5]]: ...


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
) -> AsyncIterator[tuple[T1, T2, T3, T4, T5, T6]]: ...


@overload
def azip(*aiterables: AsyncIterable[T], strict: bool = False) -> AsyncIterator[tuple[T, ...]]: ...


def azip(*aiterables: AsyncIterable[Any], strict: bool = False) -> AsyncIterator[tuple[Any, ...]]:
    """Iterate over several iterables in parallel, producing tuples with an item from each one.

    Parameters
    ----------
    *aiterables : AsyncIterable[T]
        Iterables.

    strict : bool, default False
        Strictness.

    Returns
    -------
    AsyncIterator[tuple[T, ...]]
        Iterator.

    Notes
    -----
    * If ``strict`` is :obj:`True` and iterator lengths differ, then raises :exc:`ValueError`.

    Examples
    --------
    >>> xs = arange(42)
    >>> ys = arange(4, 23)
    >>> [(x, y) async for x, y in azip(xs, ys)]
    [(0, 4), (1, 5), (2, 6), ..., (18, 22)]
    """
    if not aiterables:
        detail = "'*aiterables' must be non-empty"
        raise ValueError(detail)

    for aiterable in aiterables:
        if not isinstance(aiterable, AsyncIterable):
            detail = "'*aiterables' must be 'AsyncIterable'"
            raise TypeError(detail)

    if not isinstance(strict, bool):
        detail = "'strict' must be 'bool'"
        raise TypeError(detail)

    aiterators = [aiter(aiterable) for aiterable in aiterables]
    return AzipIterator(aiterators, strict)


@dataclass(repr=False)
class AzipIterator(AioplusIterator[tuple[T, ...]]):
    """An asynchronous iterator."""

    aiterators: list[AsyncIterator[T]]
    strict: bool

    async def __aioplus__(self) -> tuple[T, ...]:
        """Return the next value."""
        async with TaskGroup() as task_group:
            coroutines = [anext(aiterator, ...) for aiterator in self.aiterators]
            tasks = [task_group.create_task(coroutine) for coroutine in coroutines]

        maybe_results = [task.result() for task in tasks]
        results = [result for result in maybe_results if result is not ...]

        if not results:
            raise StopAsyncIteration

        if self.strict and len(results) < len(self.aiterators):
            detail = "azip(): length mismatch"
            raise ValueError(detail)

        if len(results) < len(maybe_results):
            raise StopAsyncIteration

        return tuple(results)
