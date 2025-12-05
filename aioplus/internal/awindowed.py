from collections import deque
from collections.abc import AsyncIterable, AsyncIterator
from dataclasses import dataclass
from typing import Literal, TypeVar, overload

from aioplus.internal.utils.abc import AioplusIterator


T = TypeVar("T")


@overload
def awindowed(aiterable: AsyncIterable[T], /, *, n: Literal[2]) -> AsyncIterator[tuple[T, T]]: ...


@overload
def awindowed(
    aiterable: AsyncIterable[T],
    /,
    *,
    n: Literal[3],
) -> AsyncIterator[tuple[T, T, T]]: ...


@overload
def awindowed(aiterable: AsyncIterable[T], /, *, n: int) -> AsyncIterator[tuple[T, ...]]: ...


def awindowed(aiterable: AsyncIterable[T], /, *, n: int) -> AsyncIterator[tuple[T, ...]]:
    """Return a sliding window of width ``n`` over ``aiterable``.

    Parameters
    ----------
    aiterable : AsyncIterable[T]
        Iterable.

    n : int
        Width.

    Returns
    -------
    AsyncIterator[tuple[T, ...]]
        Iterator.

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

    aiterator = aiter(aiterable)
    return AwindowedIterator(aiterator, n)


@dataclass(repr=False)
class AwindowedIterator(AioplusIterator[tuple[T, ...]]):
    """An asynchronous iterator."""

    aiterator: AsyncIterator[T]
    n: int

    def __post_init__(self) -> None:
        """Initialize the object."""
        self._window: deque[T] = deque(maxlen=self.n)

    async def __aioplus__(self) -> tuple[T, ...]:
        """Return the next item."""
        while len(self._window) < self.n - 1:
            item = await anext(self.aiterator)
            self._window.append(item)

        item = await anext(self.aiterator)

        self._window.append(item)
        return tuple(self._window)
