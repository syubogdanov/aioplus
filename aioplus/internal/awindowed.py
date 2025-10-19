from collections import deque
from collections.abc import AsyncIterable, AsyncIterator
from dataclasses import dataclass
from typing import Literal, Self, TypeVar, overload


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
    """Return a sliding window of width ``n`` over ``aiterable``.

    Parameters
    ----------
    aiterable : AsyncIterable[T]
        The asynchronous iterable.

    n : int
        The width.

    Returns
    -------
    AsyncIterable[tuple[T, ...]]
        The asynchronous iterable.

    Examples
    --------
    >>> aiterable = arange(23)
    >>> [window async for window in awindowed(aiterable, n=3)]
    [(0, 1, 2), (1, 2, 3), ..., (19, 20, 21), (20, 21, 22)]
    """
    if not isinstance(aiterable, AsyncIterable):
        detail = "'aiterable' must be 'AsyncIterable'"
        raise TypeError(detail)

    if not isinstance(n, int):
        detail = "'n' must be 'int'"
        raise TypeError(detail)

    if n <= 0:
        detail = "'n' must be positive"
        raise ValueError(detail)

    return AwindowedIterable(aiterable, n=n)


@dataclass(repr=False)
class AwindowedIterable(AsyncIterable[tuple[T, ...]]):
    """An asynchronous iterable."""

    aiterable: AsyncIterable[T]
    n: int

    def __aiter__(self) -> AsyncIterator[tuple[T, ...]]:
        """Return an asynchronous iterator."""
        aiterator = aiter(self.aiterable)
        return AwindowedIterator(aiterator, self.n)


@dataclass(repr=False)
class AwindowedIterator(AsyncIterator[tuple[T, ...]]):
    """An asynchronous iterator."""

    aiterator: AsyncIterator[T]
    n: int

    def __post_init__(self) -> None:
        """Initialize the object."""
        self._finished_flg: bool = False
        self._window: deque[T] = deque(maxlen=self.n)

    def __aiter__(self) -> Self:
        """Return an asynchronous iterator."""
        return self

    async def __anext__(self) -> tuple[T, ...]:
        """Return the next item."""
        if self._finished_flg:
            raise StopAsyncIteration

        try:
            while len(self._window) < self.n - 1:
                item = await anext(self.aiterator)
                self._window.append(item)

        except (StopAsyncIteration, BaseException):
            self._finished_flg = True
            self._window.clear()
            raise

        try:
            item = await anext(self.aiterator)

        except (StopAsyncIteration, BaseException):
            self._finished_flg = True
            self._window.clear()
            raise

        self._window.append(item)
        return tuple(self._window)
