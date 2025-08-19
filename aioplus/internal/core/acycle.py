import asyncio

from collections.abc import AsyncIterable, AsyncIterator
from dataclasses import dataclass
from typing import Self, TypeVar

from aioplus.internal.utils.coercions import to_async_iterable


T = TypeVar("T")


def acycle(aiterable: AsyncIterable[T]) -> AsyncIterable[T]:
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
    >>> import asyncio
    >>>
    >>> from aioplus import acycle, arange
    >>>
    >>> async def main() -> None:
    >>>     '''Run the program.'''
    >>>     async for num in acycle(arange(23)):
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
    :func:`itertools.cycle`
    """
    aiterable = to_async_iterable(aiterable, variable_name="aiterable")

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
        self._initialized_flg: bool = False
        self._finished_flg: bool = False
        self._values: list[T] = []
        self._next_index: int = 0

    def __aiter__(self) -> Self:
        """Return an asynchronous iterator."""
        return self

    async def __anext__(self) -> T:
        """Return the next value."""
        if self._finished_flg:
            raise StopAsyncIteration

        if self._initialized_flg:
            value = self._values[self._next_index]

            self._next_index += 1
            self._next_index %= len(self._values)

            # Move to the next coroutine!
            await asyncio.sleep(0)

            return value

        try:
            value = await anext(self.aiterator)

        except StopAsyncIteration:
            self._initialized_flg = True

            if not self._values:
                self._finished_flg = True
                raise

            value = self._values[self._next_index]

            self._next_index += 1
            self._next_index %= len(self._values)

            return value

        except Exception:
            self._initialized_flg = True
            self._finished_flg = True
            raise

        self._values.append(value)
        return value
