from collections.abc import AsyncIterable, AsyncIterator
from dataclasses import dataclass
from typing import Self, TypeVar


T = TypeVar("T")


def aenumerate(aiterable: AsyncIterable[T], /, start: int = 0) -> AsyncIterable[tuple[int, T]]:
    """Enumerate ``aiterable``.

    Parameters
    ----------
    aiterable : AsyncIterable[T]
        The asynchronous iterable.

    start : int, default 0
        The starting index.

    Returns
    -------
    AsyncIterable[tuple[int, T]]
        The asynchronous iterable.

    Examples
    --------
    >>> aiterable = arange(4, 23)
    >>> [(index, num) async for index, num in aenumerate(aiterable)]
    [(0, 4), (1, 5), (2, 6), (3, 7), ..., (17, 21), (18, 22)]

    See Also
    --------
    :func:`enumerate`
    """
    if not isinstance(aiterable, AsyncIterable):
        detail = "'aiterable' must be 'AsyncIterable'"
        raise TypeError(detail)

    if not isinstance(start, int):
        detail = "'start' must be 'int'"
        raise TypeError(detail)

    return AenumerateIterable(aiterable, start)


@dataclass(repr=False)
class AenumerateIterable(AsyncIterable[tuple[int, T]]):
    """An asynchronous iterable."""

    aiterable: AsyncIterable[T]
    start: int

    def __aiter__(self) -> AsyncIterator[tuple[int, T]]:
        """Return an asynchronous iterator."""
        aiterator = aiter(self.aiterable)
        return AenumerateIterator(aiterator, self.start)


@dataclass(repr=False)
class AenumerateIterator(AsyncIterator[tuple[int, T]]):
    """An asynchronous iterator."""

    aiterator: AsyncIterator[T]
    start: int

    def __post_init__(self) -> None:
        """Initialize the object."""
        self._next_index: int = self.start
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

        index = self._next_index
        self._next_index += 1

        return (index, value)
