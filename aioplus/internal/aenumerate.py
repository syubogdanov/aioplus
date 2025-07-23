from collections.abc import AsyncIterable, AsyncIterator
from dataclasses import dataclass
from typing import Self, SupportsIndex, TypeVar


T = TypeVar("T")


def aenumerate(
    iterable: AsyncIterable[T],
    /,
    start: SupportsIndex = 0,
) -> AsyncIterable[tuple[int, T]]:
    """Return an enumerated iterator."""
    if not isinstance(iterable, AsyncIterable):
        detail = "'iterable' must be 'AsyncIterable'"
        raise TypeError(detail)

    if not isinstance(start, SupportsIndex):
        detail = "'start' must be 'SupportsIndex'"
        raise TypeError(detail)

    start = start.__index__()

    return AenumerateIterable(iterable, start)


@dataclass
class AenumerateIterable(AsyncIterable[tuple[int, T]]):
    """An enumerated asynchronous iterable."""

    iterable: AsyncIterable[T]
    start: int

    def __aiter__(self) -> AsyncIterator[tuple[int, T]]:
        """Return an asynchronous iterator."""
        iterator = aiter(self.iterable)
        return AenumerateIterator(iterator, self.start)


@dataclass
class AenumerateIterator(AsyncIterator[tuple[int, T]]):
    """An enumerated asynchronous iterator."""

    iterator: AsyncIterator[T]
    start: int

    def __post_init__(self) -> None:
        """Initialize the object."""
        self._next_count = self.start
        self._finished_flg: bool = False

    def __aiter__(self) -> Self:
        """Return an asynchronous iterator."""
        return self

    async def __anext__(self) -> tuple[int, T]:
        """Return the next value."""
        if self._finished_flg:
            raise StopAsyncIteration

        try:
            value = await anext(self.iterator)

        except StopAsyncIteration:
            self._finished_flg = True
            raise

        count = self._next_count
        self._next_count += 1

        return (count, value)
