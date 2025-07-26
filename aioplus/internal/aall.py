from collections.abc import AsyncIterable

from aioplus.internal.typing import SupportsBool


async def aall(aiterable: AsyncIterable[SupportsBool], /) -> bool:
    """
    Return :obj:`True` if all elements of the async iterable evaluate to :obj:`True`.

    Parameters
    ----------
    aiterable : AsyncIterable of SupportsBool
        An asynchronous iterable of objects supporting :func:`object.__bool__`.

    Returns
    -------
    :class:`bool`
        :obj:`True` if all elements evaluate to :obj:`True`, or if the iterable is empty.
        :obj:`False` if any element evaluates to :obj:`False`.

    Notes
    -----
    - Short-circuits on the first object that evaluates to :obj:`False`.

    See Also
    --------
    :func:`all`
    """
    async for value in aiterable:
        if not bool(value):
            return False
    return True
