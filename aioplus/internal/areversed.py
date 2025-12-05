from collections.abc import AsyncIterable, AsyncIterator
from dataclasses import dataclass
from typing import TypeVar

from aioplus.internal.utils.abc import AioplusIterator


T = TypeVar("T")


def areversed(aiterable: AsyncIterable[T], /) -> AsyncIterator[T]:
    """Return reversed ``aiterable``.

    Parameters
    ----------
    aiterable : AsyncIterable[T]
        Iterable.

    Returns
    -------
    AsyncIterator[T]
        Iterator.

    Examples
    --------
    >>> aiterable = arange(23)
    >>> [num async for num in areversed(aiterable)]
    [22, 21, 20, 19, 18, ..., 4, 3, 2, 1, 0]

    See Also
    --------
    :func:`reversed`
    """
    if not isinstance(aiterable, AsyncIterable):
        detail = "'aiterable' must be 'AsyncIterable'"
        raise TypeError(detail)

    aiterator = aiter(aiterable)
    return AreversedIterator(aiterator)


@dataclass(repr=False)
class AreversedIterator(AioplusIterator[T]):
    """An asynchronous iterator."""

    aiterator: AsyncIterator[T]

    def __post_init__(self) -> None:
        """Initialize the object."""
        self._started_flg: bool = False
        self._stack: list[T] = []

    async def __aioplus__(self) -> T:
        """Return the next item."""
        if not self._started_flg:
            self._started_flg = True
            self._stack = [item async for item in self.aiterator]

        if not self._stack:
            raise StopAsyncIteration

        return self._stack.pop()
