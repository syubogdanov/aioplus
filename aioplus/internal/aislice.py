from collections.abc import AsyncIterable, AsyncIterator
from dataclasses import dataclass
from typing import Self, SupportsIndex, TypeVar, overload


T = TypeVar("T")


@overload
def aislice(iterable: AsyncIterable[T], stop: SupportsIndex, /) -> AsyncIterable[T]: ...


@overload
def aislice(
    iterable: AsyncIterable[T],
    start: SupportsIndex,
    stop: SupportsIndex,
    /,
) -> AsyncIterable[T]: ...


@overload
def aislice(
    iterable: AsyncIterable[T],
    start: SupportsIndex,
    stop: SupportsIndex,
    step: SupportsIndex,
    /,
) -> AsyncIterable[T]: ...


def aislice(
    iterable: AsyncIterable[T],
    start: SupportsIndex,
    stop: SupportsIndex | None = None,
    step: SupportsIndex | None = None,
    /,
) -> AsyncIterable[T]:
    """Return selected elements from the iterable."""
    if not isinstance(iterable, AsyncIterable):
        detail = "'iterable' must be 'AsyncIterable'"
        raise TypeError(detail)

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

    if start < 0:
        detail = "'start' must be non-negative"
        raise ValueError(detail)

    if stop < 0:
        detail = "'start' must be non-negative"
        raise ValueError(detail)

    if step <= 0:
        detail = "'step' must be positive"
        raise ValueError(detail)

    return IsliceIterable(iterable, start, stop, step)


@dataclass
class IsliceIterable(AsyncIterable[T]):
    """An asynchronous slice iterable."""

    iterable: AsyncIterable[T]
    start: int
    stop: int
    step: int

    def __aiter__(self) -> AsyncIterator[T]:
        """Return an asynchronous iterator."""
        iterator = aiter(self.iterable)
        return IsliceIterator(iterator, self.start, self.stop, self.step)


@dataclass
class IsliceIterator(AsyncIterator[T]):
    """An asynchronous slice iterator."""

    iterator: AsyncIterator[T]
    start: int
    stop: int
    step: int

    def __post_init__(self) -> None:
        """Initialize the object."""
        self._index: int = 0

    def __aiter__(self) -> Self:
        """Return an asynchronous iterator."""
        return self

    async def __anext__(self) -> T:
        """Return the next value."""
        while self._index < self.start:
            await anext(self.iterator)
            self._index += 1

        if self._index >= self.stop:
            raise StopAsyncIteration

        value = await anext(self.iterator)
        self._index += 1

        for _ in range(self.step - 1):
            await anext(self.iterator)
            self._index += 1

        return value
