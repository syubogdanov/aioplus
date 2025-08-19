from collections.abc import AsyncIterable
from typing import TypeVar

from aioplus.internal.awindowed import awindowed
from aioplus.internal.coercions import to_async_iterable


T = TypeVar("T")


def atriplewise(aiterable: AsyncIterable[T], /) -> AsyncIterable[tuple[T, T, T]]:
    """Return successive overlapping triplets taken from the input ``aiterable``.

    Parameters
    ----------
    aiterable : AsyncIterable of T
        An asynchronous iterable of elements to be triplet.

    Returns
    -------
    AsyncIterable of tuple[T, T, T]
        An asynchronous iterable yielding triplets of elements.

    Examples
    --------
    >>> import asyncio
    >>>
    >>> from aioplus import arange, atriplewise
    >>>
    >>> async def main() -> None:
    >>>     '''Run the program.'''
    >>>     async for left, middle, right in atriplewise(arange(23)):
    >>>         print(f'triplet = ({left}, {middle}, {right})')
    >>>
    >>> if __name__ == '__main__':
    >>>     asyncio.run(main())
    """
    aiterable = to_async_iterable(aiterable, variable_name="aiterable")

    return awindowed(aiterable, n=3)
