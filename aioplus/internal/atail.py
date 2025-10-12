import asyncio

from collections import deque
from collections.abc import AsyncIterable, AsyncIterator
from dataclasses import dataclass
from typing import Self, TypeVar


T = TypeVar("T")


def atail(aiterable: AsyncIterable[T], /, *, n: int) -> AsyncIterable[T]:
    """Return the last ``n`` items of the ``aiterable``.

    Parameters
    ----------
    aiterable : AsyncIterable[T]
        The asynchronous iterable.

    n : int
        The number of items.

    Returns
    -------
    AsyncIterable[T]
        The asynchronous iterable.

    Examples
    --------
    >>> aiterable = arange(23)
    >>> [num async for num in atail(aiterable, n=4)]
    [19, 20, 21, 22]

    Notes
    -----
    - The last ``n`` items are buffered in memory before yielding;
    - Yields control to the event loop before producing each value.
    """
    if not isinstance(aiterable, AsyncIterable):
        detail = "'aiterable' must be 'AsyncIterable'"
        raise TypeError(detail)

    if not isinstance(n, int):
        detail = "'n' must be 'int'"
        raise TypeError(detail)

    if n < 0:
        detail = "'n' must be non-negative"
        raise ValueError(detail)

    return AtailIterable(aiterable, n)


@dataclass(repr=False)
class AtailIterable(AsyncIterable[T]):
    """An asynchronous iterable."""

    aiterable: AsyncIterable[T]
    n: int

    def __aiter__(self) -> AsyncIterator[T]:
        """Return an asynchronous iterator."""
        aiterator = aiter(self.aiterable)
        return AtailIterator(aiterator, self.n)


@dataclass(repr=False)
class AtailIterator(AsyncIterator[T]):
    """An asynchronous iterator."""

    aiterator: AsyncIterable[T]
    n: int

    def __post_init__(self) -> None:
        """Initialize the object."""
        self._started_flg: bool = False
        self._finished_flg: bool = False
        self._deque: deque[T] = deque(maxlen=self.n)

    def __aiter__(self) -> Self:
        """Return an asynchronous iterator."""
        return self

    async def __anext__(self) -> T:
        """Return the next value."""
        if self._finished_flg:
            raise StopAsyncIteration

        if not self._started_flg:
            self._started_flg = True
            async for value in self.aiterator:
                self._deque.append(value)

        if not self._deque:
            self._finished_flg = True
            raise StopAsyncIteration

        value = self._deque.popleft()

        # Move to the next coroutine!
        await asyncio.sleep(0.0)

        return value
