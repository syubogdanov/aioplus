from collections.abc import AsyncIterable

from aioplus.internal.typing import SupportsBool


async def aall(aiterable: AsyncIterable[SupportsBool], /) -> bool:
    """Return :obj:`True` if all items of ``aiterable`` evaluate to :obj:`True`.

    Parameters
    ----------
    aiterable : AsyncIterable[SupportsBool]
        The asynchronous iterable.

    Returns
    -------
    :class:`bool`
        :obj:`True` if all items evaluate to :obj:`True`, or if the iterable is empty.
        :obj:`False` otherwise.

    Examples
    --------
    >>> aiterable = arange(23)
    >>> await aall(aiterable)
    False

    Notes
    -----
    * Short-circuits on the first item that evaluates to :obj:`False`.

    See Also
    --------
    :func:`all`
    """
    if not isinstance(aiterable, AsyncIterable):
        detail = "'aiterable' must be 'AsyncIterable'"
        raise TypeError(detail)

    async for value in aiterable:
        if not value:
            return False

    return True
