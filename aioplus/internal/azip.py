import asyncio

from asyncio import create_task
from collections.abc import AsyncIterable, AsyncIterator
from dataclasses import dataclass
from typing import Any, Self, TypeVar, overload


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
    """Iterate ``*aiterables`` in parallel.

    Parameters
    ----------
    *aiterables : AsyncIterable[T]
        The asynchronous iterables.

    strict : bool, default False
        If :obj:`True`, raise :obj:`ValueError` when lengths of ``*aiterables`` differ.

    Returns
    -------
    AsyncIterable[tuple[T, ...]]
        The asynchronous iterable.

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

    return AzipIterable(aiterables, strict)


@dataclass(repr=False)
class AzipIterable(AsyncIterable[tuple[T, ...]]):
    """An asynchronous iterable."""

    aiterables: tuple[AsyncIterable[T], ...]
    strict: bool

    def __aiter__(self) -> AsyncIterator[tuple[T, ...]]:
        """Return an asynchronous iterator."""
        aiterators = [aiter(aiterable) for aiterable in self.aiterables]
        return AzipIterator(aiterators, self.strict)


@dataclass(repr=False)
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

        coroutines = [anext(aiterator, ...) for aiterator in self.aiterators]
        tasks = [create_task(coroutine) for coroutine in coroutines]

        await asyncio.gather(*tasks, return_exceptions=True)

        results: list[T] = []

        exceptions: list[Exception] = []
        base_exceptions: list[BaseException] = []

        for task in tasks:
            try:
                maybe_result = task.result()

            except ExceptionGroup as group:
                exceptions.extend(group.exceptions)
            except BaseExceptionGroup as group:
                base_exceptions.extend(group.exceptions)

            except Exception as exception:
                exceptions.append(exception)
            except BaseException as exception:
                base_exceptions.append(exception)

            else:
                if maybe_result is not ...:
                    results.append(maybe_result)

        if base_exceptions:
            self._finished_flg = True
            detail = "azip(): base exception(-s) occurred"
            raise BaseExceptionGroup(detail, [*base_exceptions, *exceptions])

        if exceptions:
            self._finished_flg = True
            detail = "azip(): exception(-s) occurred"
            raise ExceptionGroup(detail, exceptions)

        if not results:
            self._finished_flg = True
            raise StopAsyncIteration

        if self.strict and len(results) < len(self.aiterators):
            self._finished_flg = True
            detail = "azip(): len(*aiterables) differ"
            raise ValueError(detail)

        if len(results) < len(self.aiterators):
            self._finished_flg = True
            raise StopAsyncIteration

        return tuple(results)
