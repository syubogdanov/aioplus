import asyncio

from collections.abc import AsyncIterable, AsyncIterator
from dataclasses import dataclass
from typing import Self, TypeVar


T = TypeVar("T")


def areversed(iterable: AsyncIterable[T]) -> AsyncIterable[T]:
    """Return a reverse iterator."""
    if not isinstance(iterable, AsyncIterable):
        detail = "'iterable' must be 'AsyncIterable'"
        raise TypeError(detail)

    return AreversedIterable(iterable)


@dataclass
class AreversedIterable(AsyncIterable[T]):
    """A reversed asynchronous iterable."""

    iterable: AsyncIterable[T]

    def __aiter__(self) -> AsyncIterator[T]:
        """Return an asynchronous iterator."""
        iterator = aiter(self.iterable)
        return AreversedIterator(iterator)


@dataclass
class AreversedIterator(AsyncIterator[T]):
    """A reversed asynchronous iterator."""

    iterator: AsyncIterator[T]

    def __post_init__(self) -> None:
        """Initialize the object."""
        self._stack: list[T] = []
        self._started_flg: bool = False

    def __aiter__(self) -> Self:
        """Return an asynchronous iterator."""
        return self

    async def __anext__(self) -> T:
        """Return the next value."""
        if not self._started_flg:
            self._started_flg = True
            async for value in self.iterator:
                self._stack.append(value)

        if not self._stack:
            raise StopAsyncIteration

        # Move to the next coroutine!
        await asyncio.sleep(0.0)

        return self._stack.pop()
