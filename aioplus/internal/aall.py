from collections.abc import AsyncIterable

from aioplus.internal.utils.typing import SupportsBool


async def aall(aiterable: AsyncIterable[SupportsBool], /) -> bool:
    """Return :obj:`True` if all items of ``aiterable`` evaluate to :obj:`True`.

    Parameters
    ----------
    aiterable : AsyncIterable[SupportsBool]
        Iterable.

    Returns
    -------
    :class:`bool`
        :obj:`True` if all items evaluate to :obj:`True`, otherwise :obj:`False`.

    Examples
    --------
    >>> aiterable = arange(23)
    >>> await aall(aiterable)
    False

    Notes
    -----
    * If ``aiterable`` is empty, then :obj:`True` is returned.

    See Also
    --------
    :func:`all`
    """
    if not isinstance(aiterable, AsyncIterable):
        detail = "'aiterable' must be 'AsyncIterable'"
        raise TypeError(detail)

    async for item in aiterable:
        if not item:
            return False

    return True
