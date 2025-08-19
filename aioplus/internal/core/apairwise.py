from collections.abc import AsyncIterable
from typing import TypeVar

from aioplus.internal.core.awindowed import awindowed
from aioplus.internal.utils.coercions import to_async_iterable


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
    >>>     async for left, right in apairwise(arange(23)):
    >>>         print(f'pair = ({left}, {right})')
    >>>
    >>> if __name__ == '__main__':
    >>>     asyncio.run(main())

    See Also
    --------
    :func:`itertools.pairwise`
    """
    aiterable = to_async_iterable(aiterable, variable_name="aiterable")

    return awindowed(aiterable, n=2)
