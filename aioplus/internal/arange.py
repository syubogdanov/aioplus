import sys

from collections.abc import AsyncIterable, AsyncIterator, Iterable, Iterator
from dataclasses import dataclass
from typing import SupportsIndex, overload

from aioplus.internal.ayield import ayield


if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self


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
) -> AsyncIterable[SupportsIndex]:
    """An asynchronous range."""  # noqa: D401
    if not isinstance(start, SupportsIndex):
        detail = f"'{type(start).__name__}' object cannot be interpreted as an integer"
        raise TypeError(detail)

    if stop is not None and not isinstance(stop, SupportsIndex):
        detail = f"'{type(stop).__name__}' object cannot be interpreted as an integer"
        raise TypeError(detail)

    if step is not None and not isinstance(step, SupportsIndex):
        detail = f"'{type(step).__name__}' object cannot be interpreted as an integer"
        raise TypeError(detail)

    if stop is None:
        stop = start
        start = 0
        step = 1

    if step is None:
        step = 1

    if step == 0:
        detail = "arange() arg 3 must not be zero"
        raise ValueError(detail)

    start = start.__index__()
    stop = stop.__index__()
    step = step.__index__()

    iterable = range(start, stop, step)
    return AsyncRangeIterable(iterable)


@dataclass
class AsyncRangeIterable(AsyncIterable[int]):
    """An asynchronous range iterable."""

    iterable: Iterable[int]

    def __aiter__(self) -> AsyncIterator[int]:
        """Return an asynchronous iterator."""
        iterator = iter(self.iterable)
        return AsyncRangeIterator(iterator)


@dataclass
class AsyncRangeIterator(AsyncIterator[int]):
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

        await ayield()
        return value
