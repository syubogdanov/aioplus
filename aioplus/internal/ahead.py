from collections.abc import AsyncIterable
from typing import TypeVar

from aioplus.internal.aislice import aislice


T = TypeVar("T")


def ahead(aiterable: AsyncIterable[T], /, *, n: int) -> AsyncIterable[T]:
    """Return the first ``n`` items of ``aiterable``.

    Parameters
    ----------
    aiterable : AsyncIterable[T]
        The asynchronous iterable.

    n : int
        The number of items.

    Returns
    -------
    AsyncIterable[T]
        The asynchronous iterable.

    Examples
    --------
    >>> aiterable = arange(23)
    >>> [num async for num in ahead(aiterable, n=4)]
    [0, 1, 2, 3]

    See Also
    --------
    :func:`itertools.islice`
    """
    if not isinstance(aiterable, AsyncIterable):
        detail = "'aiterable' must be 'AsyncIterable'"
        raise TypeError(detail)

    if not isinstance(n, int):
        detail = "'n' must be 'int'"
        raise TypeError(detail)

    if n < 0:
        detail = "'n' must be non-negative"
        raise ValueError(detail)

    return aislice(aiterable, n)
