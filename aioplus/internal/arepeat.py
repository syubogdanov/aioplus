import asyncio

from collections.abc import AsyncIterable, AsyncIterator
from dataclasses import dataclass
from typing import Self, SupportsIndex, TypeVar


T = TypeVar("T")


def arepeat(
    obj: T,
    /,
    *,
    times: SupportsIndex | None = None,
) -> AsyncIterable[T]:
    """Yield the same object repeatedly, either infinitely or a fixed number of times.

    Parameters
    ----------
    obj : T
        The object to yield repeatedly.

    times : int, optional
        Number of repetitions. Must be an object supporting :meth:`object.__index__`.
        If :obj:`None`, the object is yielded indefinitely.

    Returns
    -------
    AsyncIterable of T
        An asynchronous iterable yielding the same object multiple times.

    Examples
    --------
    >>> import asyncio
    >>>
    >>> from aioplus import arepeat
    >>>
    >>> async def main() -> None:
    >>>     '''Run the program.'''
    >>>     async for num in arepeat(23, times=4):
    >>>         print(num)
    >>>
    >>> if __name__ == '__main__':
    >>>     asyncio.run(main())

    See Also
    --------
    :func:`itertools.repeat`
    """
    if times is not None and not isinstance(times, SupportsIndex):
        detail = "'times' must be 'SupportsIndex'"
        raise TypeError(detail)

    if times is not None:
        times = times.__index__()

    if times is not None and not isinstance(times, int):
        detail = "'times.__index__()' must be 'int'"
        raise TypeError(detail)

    if times is not None and times < 0:
        detail = "'times' must be non-negative"
        raise ValueError(detail)

    return ArepeatIterable(obj, times)


@dataclass
class ArepeatIterable(AsyncIterable[T]):
    """An repeated asynchronous iterable."""

    obj: T
    times: int | None

    def __aiter__(self) -> AsyncIterator[T]:
        """Return an asynchronous iterator."""
        return ArepeatIterator(self.obj, self.times)


@dataclass
class ArepeatIterator(AsyncIterator[T]):
    """An repeated asynchronous iterator."""

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
