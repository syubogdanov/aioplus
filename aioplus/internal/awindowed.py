from collections.abc import AsyncIterable, AsyncIterator
from dataclasses import dataclass
from typing import Literal, Self, TypeVar, overload

from aioplus.internal.coercions import to_async_iterable, to_positive_int


T = TypeVar("T")


@overload
def awindowed(aiterable: AsyncIterable[T], /, *, n: Literal[1]) -> AsyncIterable[tuple[T]]: ...


@overload
def awindowed(aiterable: AsyncIterable[T], /, *, n: Literal[2]) -> AsyncIterable[tuple[T, T]]: ...


@overload
def awindowed(
    aiterable: AsyncIterable[T],
    /,
    *,
    n: Literal[3],
) -> AsyncIterable[tuple[T, T, T]]: ...


@overload
def awindowed(
    aiterable: AsyncIterable[T],
    /,
    *,
    n: Literal[4],
) -> AsyncIterable[tuple[T, T, T, T]]: ...


@overload
def awindowed(
    aiterable: AsyncIterable[T],
    /,
    *,
    n: Literal[5],
) -> AsyncIterable[tuple[T, T, T, T, T]]: ...


@overload
def awindowed(aiterable: AsyncIterable[T], /, *, n: int) -> AsyncIterable[tuple[T, ...]]: ...


def awindowed(aiterable: AsyncIterable[T], /, *, n: int) -> AsyncIterable[tuple[T, ...]]:
    """Return a sliding window of width ``n`` over the given ``aiterable``.

    Parameters
    ----------
    aiterable : AsyncIterable of T
        An asynchronous iterable of elements to be windowed.

    Returns
    -------
    AsyncIterable of tuple[T, ...]
        An asynchronous iterable yielding windows of elements.

    Examples
    --------
    >>> import asyncio
    >>>
    >>> from aioplus import arange, awindowed
    >>>
    >>> async def main() -> None:
    >>>     '''Run the program.'''
    >>>     async for left, middle, right in awindowed(arange(23), n=3):
    >>>         print(f'window = ({left}, {middle}, {right})')
    >>>
    >>> if __name__ == '__main__':
    >>>     asyncio.run(main())
    """
    aiterable = to_async_iterable(aiterable, variable_name="aiterable")
    n = to_positive_int(n, variable_name="n")

    return AwindowedIterable(aiterable, n=n)


@dataclass
class AwindowedIterable(AsyncIterable[tuple[T, ...]]):
    """An asynchronous iterable that windows data."""

    aiterable: AsyncIterable[T]
    n: int

    def __aiter__(self) -> AsyncIterator[tuple[T, ...]]:
        """Return an asynchronous iterator."""
        aiterator = aiter(self.aiterable)
        return AwindowedIterator(aiterator, self.n)


@dataclass
class AwindowedIterator(AsyncIterator[tuple[T, ...]]):
    """An asynchronous iterator that windows data."""

    aiterator: AsyncIterator[T]
    n: int

    def __post_init__(self) -> None:
        """Initialize the object."""
        raise NotImplementedError

    def __aiter__(self) -> Self:
        """Return an asynchronous iterator."""
        return self

    async def __anext__(self) -> tuple[T, ...]:
        """Return the next value."""
        raise NotImplementedError
