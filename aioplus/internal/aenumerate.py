from collections.abc import AsyncIterable, AsyncIterator
from typing import TypeVar

from aioplus.internal.acount import acount
from aioplus.internal.azip import azip


T = TypeVar("T")


def aenumerate(aiterable: AsyncIterable[T], /, start: int = 0) -> AsyncIterator[tuple[int, T]]:
    """Enumerate ``aiterable``.

    Parameters
    ----------
    aiterable : AsyncIterable[T]
        Iterable.

    start : int, default 0
        Start.

    Returns
    -------
    AsyncIterator[tuple[int, T]]
        Iterator.

    Examples
    --------
    >>> aiterable = arange(4, 23)
    >>> [(index, num) async for index, num in aenumerate(aiterable)]
    [(0, 4), (1, 5), (2, 6), (3, 7), ..., (17, 21), (18, 22)]

    See Also
    --------
    :func:`enumerate`
    """
    if not isinstance(aiterable, AsyncIterable):
        detail = "'aiterable' must be 'AsyncIterable'"
        raise TypeError(detail)

    if not isinstance(start, int):
        detail = "'start' must be 'int'"
        raise TypeError(detail)

    return azip(acount(start), aiterable)
