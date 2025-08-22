from collections.abc import AsyncIterable
from typing import Any

from aioplus.internal import coercions


async def alen(aiterable: AsyncIterable[Any], /) -> int:
    """Return length of the iterable.

    Parameters
    ----------
    aiterable : AsyncIterable[Any]
        An asynchronous iterable of objects.

    Returns
    -------
    :class:`int`
        Length of the iterable.

    Examples
    --------
    >>> aiterable = arange(23)
    >>> await alen(aiterable)
    23

    See Also
    --------
    :func:`len`
    """
    aiterable = coercions.be_async_iterable(aiterable, variable_name="aiterable")

    count = 0
    async for _ in aiterable:
        count += 1

    return count
