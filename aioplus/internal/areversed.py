import asyncio

from collections.abc import AsyncIterable, AsyncIterator
from dataclasses import dataclass
from typing import Self, TypeVar

from aioplus.internal.coercions import to_async_iterable


T = TypeVar("T")


def areversed(aiterable: AsyncIterable[T], /) -> AsyncIterable[T]:
    """Return a reverse iterator.

    Parameters
    ----------
    aiterable : AsyncIterable of T
        An asynchronous iterable to be reversed.

    Returns
    -------
    AsyncIterable of T
        An asynchronous iterable yielding the objects in reverse order.

    Examples
    --------
    >>> import asyncio
    >>>
    >>> from aioplus import arange, areversed
    >>>
    >>> async def main() -> None:
    >>>     '''Run the program.'''
    >>>     async for num in areversed(arange(2304)):
    >>>         print(num)
    >>>
    >>> if __name__ == '__main__':
    >>>     asyncio.run(main())

    Notes
    -----
    - Entire iterable is buffered in memory before yielding results;
    - Yields control to the event loop before producing each value.

    See Also
    --------
    :func:`reversed`
    """
    aiterable = to_async_iterable(aiterable, variable_name="aiterable")

    return AreversedIterable(aiterable)


@dataclass
class AreversedIterable(AsyncIterable[T]):
    """A reversed asynchronous iterable."""

    aiterable: AsyncIterable[T]

    def __aiter__(self) -> AsyncIterator[T]:
        """Return an asynchronous iterator."""
        aiterator = aiter(self.aiterable)
        return AreversedIterator(aiterator)


@dataclass
class AreversedIterator(AsyncIterator[T]):
    """A reversed asynchronous iterator."""

    aiterator: AsyncIterator[T]

    def __post_init__(self) -> None:
        """Initialize the object."""
        self._initialized_flg: bool = False
        self._finished_flg: bool = False
        self._stack: list[T] = []

    def __aiter__(self) -> Self:
        """Return an asynchronous iterator."""
        return self

    async def __anext__(self) -> T:
        """Return the next value."""
        if self._finished_flg:
            raise StopAsyncIteration

        if not self._initialized_flg:
            await self._initialize()

        if not self._stack:
            self._finished_flg = True
            raise StopAsyncIteration

        value = self._stack.pop()

        # Move to the next coroutine!
        await asyncio.sleep(0.0)

        return value

    async def _initialize(self) -> None:
        """Initialize the stack."""
        self._initialized_flg = True
        try:
            async for value in self.aiterator:
                self._stack.append(value)

        except Exception:
            self._finished_flg = True
            self._stack.clear()
            raise
