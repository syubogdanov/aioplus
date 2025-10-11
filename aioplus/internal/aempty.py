from collections.abc import AsyncIterable
from typing import Any


async def aempty(aiterable: AsyncIterable[Any], /) -> bool:
    """Return :obj:`True` if ``aiterable`` is empty, :obj:`False` otherwise.

    Parameters
    ----------
    aiterable : AsyncIterable[Any]
        The asynchronous iterable.

    Returns
    -------
    :class:`bool`
        The emptiness.

    Examples
    --------
    >>> aiterable = arange(23)
    >>> await aempty(aiterable)
    False

    Notes
    -----
    * Short-circuits on the first item.
    """
    if not isinstance(aiterable, AsyncIterable):
        detail = "'aiterable' must be 'AsyncIterable'"
        raise TypeError(detail)

    aiterator = aiter(aiterable)
    try:
        await anext(aiterator)

    except StopAsyncIteration:
        return True

    return False
