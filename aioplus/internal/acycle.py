import asyncio

from collections import deque
from collections.abc import AsyncIterable, AsyncIterator
from dataclasses import dataclass
from typing import Self, TypeVar


T = TypeVar("T")


def acycle(aiterable: AsyncIterable[T], /) -> AsyncIterator[T]:
    """Make ``aiterable`` looped.

    Parameters
    ----------
    aiterable : AsyncIterable[T]
        The asynchronous iterable.

    Returns
    -------
    AsyncIterator[T]
        The asynchronous iterator.

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
class AcycleIterator(AsyncIterator[T]):
    """An asynchronous iterator."""

    aiterator: AsyncIterator[T]

    def __post_init__(self) -> None:
        """Initialize the object."""
        self._deque: deque[T] = deque()
        self._initialized_flg: bool = False
        self._finished_flg: bool = False

    def __aiter__(self) -> Self:
        """Return an asynchronous iterator."""
        return self

    async def __anext__(self) -> T:
        """Return the next item."""
        if self._finished_flg:
            raise StopAsyncIteration

        if not self._initialized_flg:
            try:
                item = await anext(self.aiterator)
            except StopAsyncIteration:
                self._initialized_flg = True
            except BaseException:
                self._finished_flg = True
                self._deque.clear()
                raise
            else:
                self._deque.append(item)
                return item

        if not self._deque:
            self._finished_flg = True
            raise StopAsyncIteration

        item = self._deque.popleft()
        self._deque.append(item)

        # Move to the next coroutine!
        await asyncio.sleep(0.0)

        return item
