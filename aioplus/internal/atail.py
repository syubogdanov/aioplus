import asyncio

from collections import deque
from collections.abc import AsyncIterable, AsyncIterator
from dataclasses import dataclass
from typing import Self, SupportsIndex, TypeVar

from aioplus.internal.coercions import to_async_iterable, to_non_negative_int


T = TypeVar("T")


def atail(aiterable: AsyncIterable[T], /, *, n: SupportsIndex) -> AsyncIterable[T]:
    """Return the last ``n`` items of the ``aiterable``.

    Parameters
    ----------
    aiterable : AsyncIterable[T]
        An asynchronous iterable to retrieve items from.

    n : SupportsIndex
        The number of items to retrieve from the end.

    Returns
    -------
    AsyncIterable[T]
        An asynchronous iterable yielding the last ``n`` items of the ``aiterable``.

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
    aiterable = to_async_iterable(aiterable, variable_name="aiterable")
    n = to_non_negative_int(n, variable_name="n")

    return AtailIterable(aiterable, n)


@dataclass
class AtailIterable(AsyncIterable[T]):
    """An asynchronous iterable."""

    aiterable: AsyncIterable[T]
    n: int

    def __aiter__(self) -> AsyncIterator[T]:
        """Return an asynchronous iterator."""
        aiterator = aiter(self.aiterable)
        return AtailIterator(aiterator, self.n)


@dataclass
class AtailIterator(AsyncIterator[T]):
    """An asynchronous iterator."""

    aiterator: AsyncIterable[T]
    n: int

    def __post_init__(self) -> None:
        """Initialize the object."""
        self._prefetched_flg: bool = False
        self._finished_flg: bool = False
        self._deque: deque[T] = deque(maxlen=self.n)

    def __aiter__(self) -> Self:
        """Return an asynchronous iterator."""
        return self

    async def __anext__(self) -> T:
        """Return the next value."""
        if self._finished_flg:
            raise StopAsyncIteration

        if not self._prefetched_flg:
            await self._prefetch()

        if not self._deque:
            self._finished_flg = True
            raise StopAsyncIteration

        value = self._deque.popleft()

        # Move to the next coroutine!
        await asyncio.sleep(0.0)

        return value

    async def _prefetch(self) -> None:
        """Prefetch the deque."""
        self._prefetched_flg = True
        try:
            async for value in self.aiterator:
                self._deque.append(value)

        except Exception:
            self._finished_flg = True
            self._deque.clear()
            raise
