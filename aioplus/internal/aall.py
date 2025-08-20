from collections.abc import AsyncIterable

from aioplus.internal.coercions import to_async_iterable
from aioplus.internal.typing import SupportsBool


async def aall(aiterable: AsyncIterable[SupportsBool], /) -> bool:
    """
    Return :obj:`True` if all elements of the async iterable evaluate to :obj:`True`.

    Parameters
    ----------
    aiterable : AsyncIterable of SupportsBool
        An asynchronous iterable of objects supporting :meth:`object.__bool__`.

    Returns
    -------
    :class:`bool`
        :obj:`True` if all elements evaluate to :obj:`True`, or if the iterable is empty.
        :obj:`False` if any element evaluates to :obj:`False`.

    Examples
    --------
    >>> aiterable = arange(23)
    >>> await aall(aiterable)
    False

    Notes
    -----
    - Short-circuits on the first object that evaluates to :obj:`False`.

    See Also
    --------
    :func:`all`
    """
    aiterable = to_async_iterable(aiterable, variable_name="aiterable")

    async for value in aiterable:
        if not value:
            return False

    return True
