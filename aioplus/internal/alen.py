from collections.abc import AsyncIterable
from typing import Any


async def alen(aiterable: AsyncIterable[Any], /) -> int:
    """Return the length of an object."""
    if not isinstance(aiterable, AsyncIterable):
        detail = "'aiterable' must be 'AsyncIterable'"
        raise TypeError(detail)

    count = 0
    async for _ in aiterable:
        count += 1

    return count
