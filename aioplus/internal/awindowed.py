from collections import deque
from collections.abc import AsyncIterable, AsyncIterator
from dataclasses import dataclass
from typing import Literal, Self, TypeVar, overload

from aioplus.internal import coercions


T = TypeVar("T")


@overload
def awindowed(aiterable: AsyncIterable[T], /, *, n: Literal[2]) -> AsyncIterable[tuple[T, T]]: ...


@overload
def awindowed(
    aiterable: AsyncIterable[T],
    /,
    *,
    n: Literal[3],
) -> AsyncIterable[tuple[T, T, T]]: ...


@overload
def awindowed(aiterable: AsyncIterable[T], /, *, n: int) -> AsyncIterable[tuple[T, ...]]: ...


def awindowed(aiterable: AsyncIterable[T], /, *, n: int) -> AsyncIterable[tuple[T, ...]]:
    """Return a sliding window of width ``n`` over the given ``aiterable``.

    Parameters
    ----------
    aiterable : AsyncIterable of T
        An asynchronous iterable of elements to be windowed.

    Returns
    -------
    AsyncIterable of tuple[T, ...]
        An asynchronous iterable yielding windows of elements.

    Examples
    --------
    >>> aiterable = arange(23)
    >>> [window async for window in awindowed(aiterable, n=3)]
    [(0, 1, 2), (1, 2, 3), ..., (19, 20, 21), (20, 21, 22)]
    """
    aiterable = coercions.be_async_iterable(aiterable, variable_name="aiterable")
    n = coercions.be_positive_int(n, variable_name="n")

    return AwindowedIterable(aiterable, n=n)


@dataclass
class AwindowedIterable(AsyncIterable[tuple[T, ...]]):
    """An asynchronous iterable that windows data."""

    aiterable: AsyncIterable[T]
    n: int

    def __aiter__(self) -> AsyncIterator[tuple[T, ...]]:
        """Return an asynchronous iterator."""
        aiterator = aiter(self.aiterable)
        return AwindowedIterator(aiterator, self.n)


@dataclass
class AwindowedIterator(AsyncIterator[tuple[T, ...]]):
    """An asynchronous iterator that windows data."""

    aiterator: AsyncIterator[T]
    n: int

    def __post_init__(self) -> None:
        """Initialize the object."""
        self._window: deque[T] = deque(maxlen=self.n)
        self._prefetched_flg: bool = False
        self._finished_flg: bool = False

    def __aiter__(self) -> Self:
        """Return an asynchronous iterator."""
        return self

    async def __anext__(self) -> tuple[T, ...]:
        """Return the next value."""
        if self._finished_flg:
            raise StopAsyncIteration

        if not self._prefetched_flg:
            await self._prefetch()

        try:
            value = await anext(self.aiterator)

        except Exception:
            self._finished_flg = True
            self._window.clear()
            raise

        self._window.append(value)
        return tuple(self._window)

    async def _prefetch(self) -> None:
        """Prefetch the window."""
        self._prefetched_flg = True
        try:
            for _ in range(self.n - 1):
                value = await anext(self.aiterator)
                self._window.append(value)

        except Exception:
            self._finished_flg = True
            self._window.clear()
            raise
