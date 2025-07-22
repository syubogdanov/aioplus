from collections.abc import AsyncIterable, AsyncIterator
from dataclasses import dataclass
from typing import Self, SupportsIndex


def acount(
    start: SupportsIndex = 0,
    step: SupportsIndex = 1,
) -> AsyncIterable[int]:
    """Return evenly spaced values beginning with `start`."""
    if not isinstance(start, SupportsIndex):
        detail = "'start' must be 'SupportsIndex'"
        raise TypeError(detail)

    if not isinstance(step, SupportsIndex):
        detail = "'step' must be 'SupportsIndex'"
        raise TypeError(detail)

    start = start.__index__()
    step = step.__index__()

    return AcountIterable(start, step)


@dataclass
class AcountIterable(AsyncIterable[int]):
    """An asynchronous iterable."""

    start: int
    step: int

    def __aiter__(self) -> AsyncIterator[int]:
        """Return an asynchronous iterator."""
        return AcountIterator(self.start, self.step)


@dataclass
class AcountIterator(AsyncIterator[int]):
    """An asynchronous iterator."""

    start: int
    step: int

    def __post_init__(self) -> None:
        """Initialize the object."""
        self._previous = self.start - self.start

    def __aiter__(self) -> Self:
        """Return an asynchronous iterator."""
        return self

    async def __anext__(self) -> int:
        """Return the next value."""
        self._previous += self.step
        return self._previous
