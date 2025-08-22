from collections.abc import AsyncIterable
from typing import TypeVar

from aioplus.internal import coercions
from aioplus.internal.awindowed import awindowed


T = TypeVar("T")


def apairwise(aiterable: AsyncIterable[T], /) -> AsyncIterable[tuple[T, T]]:
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
    >>> aiterable = arange(23)
    >>> [pair async for pair in apairwise(aiterable)]
    [(0, 1), (1, 2), (2, 3), ..., (20, 21), (21, 22)]

    See Also
    --------
    :func:`itertools.pairwise`
    """
    aiterable = coercions.be_async_iterable(aiterable, variable_name="aiterable")

    return awindowed(aiterable, n=2)
