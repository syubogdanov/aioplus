import asyncio

from collections.abc import AsyncIterable, AsyncIterator
from dataclasses import dataclass
from typing import Self, TypeVar


T = TypeVar("T")


def areversed(aiterable: AsyncIterable[T], /) -> AsyncIterable[T]:
    """Return reversed ``aiterable``.

    Parameters
    ----------
    aiterable : AsyncIterable[T]
        The asynchronous iterable.

    Returns
    -------
    AsyncIterable of T
        The asynchronous iterable.

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

    return AreversedIterable(aiterable)


@dataclass(repr=False)
class AreversedIterable(AsyncIterable[T]):
    """A asynchronous iterable."""

    aiterable: AsyncIterable[T]

    def __aiter__(self) -> AsyncIterator[T]:
        """Return an asynchronous iterator."""
        aiterator = aiter(self.aiterable)
        return AreversedIterator(aiterator)


@dataclass(repr=False)
class AreversedIterator(AsyncIterator[T]):
    """A asynchronous iterator."""

    aiterator: AsyncIterator[T]

    def __post_init__(self) -> None:
        """Initialize the object."""
        self._started_flg: bool = False
        self._finished_flg: bool = False
        self._stack: list[T] = []

    def __aiter__(self) -> Self:
        """Return an asynchronous iterator."""
        return self

    async def __anext__(self) -> T:
        """Return the next value."""
        if self._finished_flg:
            raise StopAsyncIteration

        try:
            if not self._started_flg:
                self._started_flg = True
                async for value in self.aiterator:
                    self._stack.append(value)

        except Exception:
            self._finished_flg = True
            raise

        if not self._stack:
            self._finished_flg = True
            raise StopAsyncIteration

        value = self._stack.pop()

        # Move to the next coroutine!
        await asyncio.sleep(0.0)

        return value
