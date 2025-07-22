import asyncio

from collections.abc import AsyncIterable, AsyncIterator, Iterable, Iterator
from dataclasses import dataclass
from typing import Self, SupportsIndex, overload


@overload
def arange(stop: SupportsIndex, /) -> AsyncIterable[int]: ...


@overload
def arange(start: SupportsIndex, stop: SupportsIndex, /) -> AsyncIterable[int]: ...


@overload
def arange(
    start: SupportsIndex,
    stop: SupportsIndex,
    step: SupportsIndex,
    /,
) -> AsyncIterable[int]: ...


def arange(
    start: SupportsIndex,
    stop: SupportsIndex | None = None,
    step: SupportsIndex | None = None,
    /,
) -> AsyncIterable[int]:
    """Iterate over a range of integers."""
    if stop is None:
        stop = start
        start = 0
        step = 1

    if step is None:
        step = 1

    if not isinstance(start, SupportsIndex):
        detail = "'start' must be 'SupportsIndex'"
        raise TypeError(detail)

    if not isinstance(step, SupportsIndex):
        detail = "'step' must be 'SupportsIndex'"
        raise TypeError(detail)

    if not isinstance(stop, SupportsIndex):
        detail = "'stop' must be 'SupportsIndex'"
        raise TypeError(detail)

    start = start.__index__()
    stop = stop.__index__()
    step = step.__index__()

    if step == 0:
        detail = "'step' must not be zero"
        raise ValueError(detail)

    iterable = range(start, stop, step)
    return ArangeIterable(iterable)


@dataclass
class ArangeIterable(AsyncIterable[int]):
    """An asynchronous range iterable."""

    iterable: Iterable[int]

    def __aiter__(self) -> AsyncIterator[int]:
        """Return an asynchronous iterator."""
        iterator = iter(self.iterable)
        return ArangeIterator(iterator)


@dataclass
class ArangeIterator(AsyncIterator[int]):
    """An asynchronous range iterator."""

    iterator: Iterator[int]

    def __aiter__(self) -> Self:
        """Return an asynchronous iterator."""
        return self

    async def __anext__(self) -> int:
        """Return the next value."""
        try:
            value = next(self.iterator)

        except StopIteration:
            raise StopAsyncIteration from None

        await asyncio.sleep(0)
        return value
