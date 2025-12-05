from collections.abc import AsyncIterable

from aioplus.internal.utils.typing import SupportsBool


async def aany(aiterable: AsyncIterable[SupportsBool], /) -> bool:
    """Return :obj:`True` if any items of ``aiterable`` evaluate to :obj:`True`.

    Parameters
    ----------
    aiterable : AsyncIterable[SupportsBool]
        Iterable.

    Returns
    -------
    :class:`bool`
        :obj:`True` if any item evaluates to :obj:`True`, otherwise :obj:`False`.

    Examples
    --------
    >>> aiterable = arange(23)
    >>> await aany(aiterable)
    True

    Notes
    -----
    * If ``aiterable`` is empty, then :obj:`False` is returned.

    See Also
    --------
    :func:`any`
    """
    if not isinstance(aiterable, AsyncIterable):
        detail = "'aiterable' must be 'AsyncIterable'"
        raise TypeError(detail)

    async for item in aiterable:
        if item:
            return True

    return False
