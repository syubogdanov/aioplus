from collections.abc import AsyncIterable, AsyncIterator
from dataclasses import dataclass
from typing import Self, TypeVar


T = TypeVar("T")


def apairwise(aiterable: AsyncIterable[T]) -> AsyncIterable[tuple[T, T]]:
    """Return successive overlapping pairs taken from the input ``aiterable``.

    Parameters
    ----------
    aiterable : AsyncIterable of T
        An asynchronous iterable of elements to be paired.

    Returns
    -------
    AsyncIterable of tuple[T, T]
        An asynchronous iterable yielding pairs of elements.

    Examples
    --------
    >>> import asyncio
    >>>
    >>> from aioplus import apairwise, arange
    >>>
    >>> async def main() -> None:
    >>>     '''Run the program.'''
    >>>     async for before, after in apairwise(arange(23)):
    >>>         print(f'{before} -> {after}')
    >>>
    >>> if __name__ == '__main__':
    >>>     asyncio.run(main())

    See Also
    --------
    :func:`itertools.pairwise`
    """
    if not isinstance(aiterable, AsyncIterable):
        detail = "'aiterable' must be 'AsyncIterable'"
        raise TypeError(detail)

    return ApairwiseIterable(aiterable)


@dataclass
class ApairwiseIterable(AsyncIterable[tuple[T, T]]):
    """An asynchronous iterable that pairs data."""

    aiterable: AsyncIterable[T]

    def __aiter__(self) -> AsyncIterator[tuple[T, T]]:
        """Return an asynchronous iterator."""
        aiterator = aiter(self.aiterable)
        return ApairwiseIterator(aiterator)


@dataclass
class ApairwiseIterator(AsyncIterator[tuple[T, T]]):
    """An asynchronous iterator that pairs data."""

    aiterator: AsyncIterator[T]

    def __post_init__(self) -> None:
        """Initialize the object."""
        self._initialized_flg: bool = False
        self._finished_flg: bool = False
        self._previous: T = object()  # type: ignore[assignment]

    def __aiter__(self) -> Self:
        """Return an asynchronous iterator."""
        return self

    async def __anext__(self) -> tuple[T, T]:
        """Return the next value."""
        if self._finished_flg:
            raise StopAsyncIteration

        try:
            value = await anext(self.aiterator)

        except Exception:
            self._finished_flg = True
            raise

        if self._initialized_flg:
            previous = self._previous
            self._previous = value
            return (previous, value)

        self._previous = value
        self._initialized_flg = True

        try:
            value = await anext(self.aiterator)

        except Exception:
            self._finished_flg = True
            raise

        previous = self._previous
        self._previous = value

        return (previous, value)
