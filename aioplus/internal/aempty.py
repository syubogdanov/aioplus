from collections.abc import AsyncIterable
from typing import Any


async def aempty(aiterable: AsyncIterable[Any], /) -> bool:
    """Return :obj:`True` if ``aiterable`` is empty, otherwise :obj:`False`.

    Parameters
    ----------
    aiterable : AsyncIterable[Any]
        Iterable.

    Returns
    -------
    :class:`bool`
        Emptiness.

    Examples
    --------
    >>> aiterable = arange(23)
    >>> await aempty(aiterable)
    False
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
