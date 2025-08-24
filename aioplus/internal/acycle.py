import asyncio

from collections import deque
from collections.abc import AsyncIterable, AsyncIterator
from dataclasses import dataclass
from typing import Self, TypeVar


T = TypeVar("T")


def acycle(aiterable: AsyncIterable[T], /) -> AsyncIterable[T]:
    """Make an iterator returning elements from the ``aiterable`` and saving a copy of each.

    Parameters
    ----------
    aiterable : AsyncIterable of T
        An asynchronous iterable of elements to be cycled.

    Returns
    -------
    AsyncIterable of T
        An asynchronous iterable yielding elements from the input iterable.

    Examples
    --------
    >>> aiterable = arange(23)
    >>> [num async for num in acycle(aiterable)]
    [0, 1, ..., 22, 23, 0, 1, ..., 22, 23, ...]

    Notes
    -----
    - Entire iterable is buffered in memory before yielding results;
    - Yields control to the event loop before producing each value.

    See Also
    --------
    :func:`itertools.cycle`
    """
    if not isinstance(aiterable, AsyncIterable):
        detail = "'aiterable' must be 'AsyncIterable'"
        raise TypeError(detail)

    return AcycleIterable(aiterable)


@dataclass
class AcycleIterable(AsyncIterable[T]):
    """An asynchronous iterable that cycles data."""

    aiterable: AsyncIterable[T]

    def __aiter__(self) -> AsyncIterator[T]:
        """Return an asynchronous iterator."""
        aiterator = aiter(self.aiterable)
        return AcycleIterator(aiterator)


@dataclass
class AcycleIterator(AsyncIterator[T]):
    """An asynchronous iterator that cycles data."""

    aiterator: AsyncIterator[T]

    def __post_init__(self) -> None:
        """Initialize the object."""
        self._deque: deque[T] = deque()
        self._prefetched_flg: bool = False
        self._finished_flg: bool = False

    def __aiter__(self) -> Self:
        """Return an asynchronous iterator."""
        return self

    async def __anext__(self) -> T:
        """Return the next value."""
        if self._finished_flg:
            raise StopAsyncIteration

        if self._prefetched_flg:
            value = self._rotate()

            # Move to the next coroutine!
            await asyncio.sleep(0)

            return value

        try:
            value = await anext(self.aiterator)

        except StopAsyncIteration:
            self._prefetched_flg = True

            if not self._deque:
                self._finished_flg = True
                raise

            return self._rotate()

        except Exception:
            self._finished_flg = True
            self._deque.clear()
            raise

        self._deque.append(value)
        return value

    def _rotate(self) -> T:
        """Rotate the deque."""
        value = self._deque.popleft()
        self._deque.append(value)
        return value
