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

    return ArangeIterable(start, stop, step)


@dataclass
class ArangeIterable(AsyncIterable[int]):
    """An asynchronous range iterable."""

    start: int
    stop: int
    step: int

    def __aiter__(self) -> AsyncIterator[int]:
        """Return an asynchronous iterator."""
        return ArangeIterator(self.start, self.stop, self.step)


@dataclass
class ArangeIterator(AsyncIterator[int]):
    """An asynchronous range iterator."""

    start: int
    stop: int
    step: int

    def __post_init__(self) -> None:
        """Initialize the object."""
        self._previous = self.start - self.step

    def __aiter__(self) -> Self:
        """Return an asynchronous iterator."""
        return self

    async def __anext__(self) -> int:
        """Return the next value."""
        self._previous += self.step

        if self.step > 0 and self._previous >= self.stop:
            raise StopAsyncIteration

        if self.step < 0 and self._previous <= self.stop:
            raise StopAsyncIteration

        return self._previous
