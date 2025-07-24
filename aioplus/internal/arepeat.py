import asyncio

from collections.abc import AsyncIterable, AsyncIterator
from dataclasses import dataclass
from typing import Self, SupportsIndex, TypeVar


T = TypeVar("T")


def arepeat(
    object_: T,
    /,
    *,
    times: SupportsIndex | None = None,
) -> AsyncIterable[T]:
    """Return an enumerated iterator."""
    if times is not None and not isinstance(times, SupportsIndex):
        detail = "'times' must be 'SupportsIndex'"
        raise TypeError(detail)

    if times is not None:
        times = times.__index__()

    if times is not None and times < 0:
        detail = "'times' must be non-negative"
        raise ValueError(detail)

    return ArepeatIterable(object_, times)


@dataclass
class ArepeatIterable(AsyncIterable[T]):
    """An repeated asynchronous iterable."""

    object_: T
    times: int | None

    def __aiter__(self) -> AsyncIterator[T]:
        """Return an asynchronous iterator."""
        return ArepeatIterator(self.object_, self.times)


@dataclass
class ArepeatIterator(AsyncIterator[T]):
    """An repeated asynchronous iterator."""

    object_: T
    times: int | None

    def __post_init__(self) -> None:
        """Initialize the object."""
        self._count: int = 0

    def __aiter__(self) -> Self:
        """Return an asynchronous iterator."""
        return self

    async def __anext__(self) -> T:
        """Return the next value."""
        if self.times is not None and self._count >= self.times:
            raise StopAsyncIteration

        self._count += 1

        # Move to the next coroutine!
        await asyncio.sleep(0.0)

        return self.object_
