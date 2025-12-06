from collections.abc import AsyncIterable
from typing import Any


async def alen(aiterable: AsyncIterable[Any], /) -> int:
    """Return length of ``aiterable``.

    Parameters
    ----------
    aiterable : AsyncIterable[Any]
        Iterable.

    Returns
    -------
    :class:`int`
        Length.

    Examples
    --------
    >>> aiterable = arange(23)
    >>> await alen(aiterable)
    23

    See Also
    --------
    :func:`len`
    """
    if not isinstance(aiterable, AsyncIterable):
        detail = "'aiterable' must be 'AsyncIterable'"
        raise TypeError(detail)

    count = 0
    async for _ in aiterable:
        count += 1

    return count
