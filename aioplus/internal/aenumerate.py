from collections.abc import AsyncIterable, AsyncIterator
from dataclasses import dataclass
from typing import Self, SupportsIndex, TypeVar

from aioplus.internal import cast


T = TypeVar("T")


def aenumerate(
    aiterable: AsyncIterable[T],
    /,
    start: SupportsIndex = 0,
) -> AsyncIterable[tuple[int, T]]:
    """Return an enumerated iterator.

    Parameters
    ----------
    aiterable : AsyncIterable of T
        An asynchronous iterable of objects to enumerate.

    start : int, default 0
        The starting index. Must be an object supporting :meth:`object.__index__`.

    Returns
    -------
    AsyncIterable of tuple[int, T]
        An asynchronous iterable yielding pairs of the form ``(index, object)``.

    Examples
    --------
    >>> import asyncio
    >>>
    >>> from aioplus import aenumerate, arange
    >>>
    >>> async def main() -> None:
    >>>     '''Run the program.'''
    >>>     async for index, num in aenumerate(arange(2304)):
    >>>         print(index, num)
    >>>
    >>> if __name__ == '__main__':
    >>>     asyncio.run(main())

    See Also
    --------
    :func:`enumerate`
    """
    if not isinstance(aiterable, AsyncIterable):
        detail = "'aiterable' must be 'AsyncIterable'"
        raise TypeError(detail)

    start = cast.to_int(start, variable_name="start")

    return AenumerateIterable(aiterable, start)


@dataclass
class AenumerateIterable(AsyncIterable[tuple[int, T]]):
    """An enumerated asynchronous iterable."""

    aiterable: AsyncIterable[T]
    start: int

    def __aiter__(self) -> AsyncIterator[tuple[int, T]]:
        """Return an asynchronous iterator."""
        aiterator = aiter(self.aiterable)
        return AenumerateIterator(aiterator, self.start)


@dataclass
class AenumerateIterator(AsyncIterator[tuple[int, T]]):
    """An enumerated asynchronous iterator."""

    aiterator: AsyncIterator[T]
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
            value = await anext(self.aiterator)

        except Exception:
            self._finished_flg = True
            raise

        count = self._next_count
        self._next_count += 1

        return (count, value)
