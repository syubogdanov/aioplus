from collections.abc import AsyncIterable
from typing import SupportsIndex, TypeVar

from aioplus.internal.aislice import aislice
from aioplus.internal.coercions import to_async_iterable, to_non_negative_int


T = TypeVar("T")


def ahead(aiterable: AsyncIterable[T], /, *, n: SupportsIndex) -> AsyncIterable[T]:
    """Return the first ``n`` items of the ``aiterable``.

    Parameters
    ----------
    aiterable : AsyncIterable[T]
        An asynchronous iterable to retrieve items from.

    n : SupportsIndex
        The number of items to retrieve from the start.

    Returns
    -------
    AsyncIterable[T]
        An asynchronous iterable yielding the first ``n`` items of the ``aiterable``.

    Examples
    --------
    >>> aiterable = arange(23)
    >>> [num async for num in ahead(aiterable, n=4)]
    [0, 1, 2, 3]

    See Also
    --------
    :func:`itertools.islice`
    """
    aiterable = to_async_iterable(aiterable, variable_name="aiterable")
    n = to_non_negative_int(n, variable_name="n")

    return aislice(aiterable, n)
