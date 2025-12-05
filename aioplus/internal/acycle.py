from collections import deque
from collections.abc import AsyncIterable, AsyncIterator
from dataclasses import dataclass
from typing import TypeVar

from aioplus.internal.utils.abc import AioplusIterator


T = TypeVar("T")


def acycle(aiterable: AsyncIterable[T], /) -> AsyncIterator[T]:
    """Repeat ``aiterable`` items indefinitely.

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
    >>> [num async for num in acycle(aiterable)]
    [0, 1, ..., 22, 23, 0, 1, ..., 22, 23, ...]

    See Also
    --------
    :func:`itertools.cycle`
    """
    if not isinstance(aiterable, AsyncIterable):
        detail = "'aiterable' must be 'AsyncIterable'"
        raise TypeError(detail)

    aiterator = aiter(aiterable)
    return AcycleIterator(aiterator)


@dataclass(repr=False)
class AcycleIterator(AioplusIterator[T]):
    """An asynchronous iterator."""

    aiterator: AsyncIterator[T]

    def __post_init__(self) -> None:
        """Initialize the object."""
        self._deque: deque[T] = deque()
        self._initialized_flg = False

    async def __aioplus__(self) -> T:
        """Return the next item."""
        if not self._initialized_flg:
            try:
                item = await anext(self.aiterator)
            except StopAsyncIteration:
                self._initialized_flg = True
            else:
                self._deque.append(item)
                return item

        if not self._deque:
            raise StopAsyncIteration

        item = self._deque.popleft()
        self._deque.append(item)

        return item
