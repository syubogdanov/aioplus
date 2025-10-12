from collections.abc import AsyncIterable

from aioplus.internal.typing import SupportsBool


async def aany(aiterable: AsyncIterable[SupportsBool], /) -> bool:
    """Return :obj:`True` if any items of ``aiterable`` evaluate to :obj:`True`.

    Parameters
    ----------
    aiterable : AsyncIterable[SupportsBool]
        The asynchronous iterable.

    Returns
    -------
    :class:`bool`
        :obj:`True` if any item evaluates to :obj:`True`.
        :obj:`False` otherwise, or if the iterable is empty.

    Examples
    --------
    >>> aiterable = arange(23)
    >>> await aany(aiterable)
    True

    See Also
    --------
    :func:`any`
    """
    if not isinstance(aiterable, AsyncIterable):
        detail = "'aiterable' must be 'AsyncIterable'"
        raise TypeError(detail)

    async for value in aiterable:
        if value:
            return True

    return False
