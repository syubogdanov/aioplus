from collections.abc import AsyncIterable
from typing import Any

from aioplus.internal.coercions import to_async_iterable


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
    aiterable = to_async_iterable(aiterable, variable_name="aiterable")

    count = 0
    async for _ in aiterable:
        count += 1

    return count
