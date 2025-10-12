import asyncio

from collections.abc import AsyncIterable, AsyncIterator
from dataclasses import dataclass
from typing import Self, TypeVar


T = TypeVar("T")


def arepeat(obj: T, /, *, times: int | None = None) -> AsyncIterable[T]:
    """Return the same object repeatedly.

    Parameters
    ----------
    obj : T
        The object.

    times : int, optional
        The number of repetitions. If :obj:`None`, then the iterable will be infinite.

    Returns
    -------
    AsyncIterable[T]
        The asynchronous iterable.

    Examples
    --------
    >>> [num async for num in arepeat(23, times=4)]
    [23, 23, 23, 23]

    See Also
    --------
    :func:`itertools.repeat`
    """
    if times is not None and not isinstance(times, int):
        detail = "'times' must be 'int' or 'None'"
        raise TypeError(detail)

    if times is not None and times < 0:
        detail = "'times' must be non-negative"
        raise ValueError(detail)

    return ArepeatIterable(obj, times)


@dataclass(repr=False)
class ArepeatIterable(AsyncIterable[T]):
    """An asynchronous iterable."""

    obj: T
    times: int | None

    def __aiter__(self) -> AsyncIterator[T]:
        """Return an asynchronous iterator."""
        return ArepeatIterator(self.obj, self.times)


@dataclass(repr=False)
class ArepeatIterator(AsyncIterator[T]):
    """An asynchronous iterator."""

    obj: T
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

        return self.obj
