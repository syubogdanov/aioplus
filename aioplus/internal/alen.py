from collections.abc import AsyncIterable
from typing import Any


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
    >>> import asyncio
    >>>
    >>> from aioplus import alen, arange
    >>>
    >>> async def main() -> None:
    >>>     aiterable = arange(2304)
    >>>     length = await alen(aiterable)
    >>>     print(f"len(aiterable) == {length}")
    >>>
    >>> if __name__ == '__main__':
    >>>     asyncio.run(main())

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
