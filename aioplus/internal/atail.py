from collections import deque
from collections.abc import AsyncIterable, AsyncIterator
from dataclasses import dataclass
from typing import TypeVar

from aioplus.internal.utils.abc import AioplusIterator


T = TypeVar("T")


def atail(aiterable: AsyncIterable[T], /, *, n: int) -> AsyncIterator[T]:
    """Return the last ``n`` items of the ``aiterable``.

    Parameters
    ----------
    aiterable : AsyncIterable[T]
        Iterable.

    n : int
        Count.

    Returns
    -------
    AsyncIterator[T]
        Iterator.

    Examples
    --------
    >>> aiterable = arange(23)
    >>> [num async for num in atail(aiterable, n=4)]
    [19, 20, 21, 22]
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

    aiterator = aiter(aiterable)
    return AtailIterator(aiterator, n)


@dataclass(repr=False)
class AtailIterator(AioplusIterator[T]):
    """An asynchronous iterator."""

    aiterator: AsyncIterable[T]
    n: int

    def __post_init__(self) -> None:
        """Initialize the object."""
        self._started_flg: bool = False
        self._deque: deque[T] = deque(maxlen=self.n)

    async def __aioplus__(self) -> T:
        """Return the next item."""
        if not self._started_flg:
            self._started_flg = True
            async for item in self.aiterator:
                self._deque.append(item)

        if not self._deque:
            raise StopAsyncIteration

        return self._deque.popleft()
