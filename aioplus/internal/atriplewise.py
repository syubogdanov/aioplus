from collections.abc import AsyncIterable
from typing import TypeVar

from aioplus.internal.awindowed import awindowed


T = TypeVar("T")


def atriplewise(aiterable: AsyncIterable[T], /) -> AsyncIterable[tuple[T, T, T]]:
    """Return a sliding window of width ``n=3`` over ``aiterable``.

    Parameters
    ----------
    aiterable : AsyncIterable[T]
        The asynchronous iterable.

    Returns
    -------
    AsyncIterable[tuple[T, T, T]]
        The asynchronous iterable.

    Examples
    --------
    >>> aiterable = arange(23)
    >>> [triplet async for triplet in atriplewise(aiterable)]
    [(0, 1, 2), (1, 2, 3), ..., (19, 20, 21), (20, 21, 22)]
    """
    if not isinstance(aiterable, AsyncIterable):
        detail = "'aiterable' must be 'AsyncIterable'"
        raise TypeError(detail)

    return awindowed(aiterable, n=3)
