from collections.abc import AsyncIterable, AsyncIterator
from typing import TypeVar

from aioplus.internal.awindowed import awindowed


T = TypeVar("T")


def apairwise(aiterable: AsyncIterable[T], /) -> AsyncIterator[tuple[T, T]]:
    """Return a sliding window of width ``n=2`` over ``aiterable``.

    Parameters
    ----------
    aiterable : AsyncIterable[T]
        The asynchronous iterable.

    Returns
    -------
    AsyncIterator[tuple[T, T]]
        The asynchronous iterator.

    Examples
    --------
    >>> aiterable = arange(23)
    >>> [pair async for pair in apairwise(aiterable)]
    [(0, 1), (1, 2), (2, 3), ..., (20, 21), (21, 22)]

    See Also
    --------
    :func:`itertools.pairwise`
    """
    if not isinstance(aiterable, AsyncIterable):
        detail = "'aiterable' must be 'AsyncIterable'"
        raise TypeError(detail)

    return awindowed(aiterable, n=2)
