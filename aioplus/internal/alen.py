from collections.abc import AsyncIterable
from typing import Any


async def alen(iterable: AsyncIterable[Any]) -> int:
    """Return the length of an object."""
    count = 0

    async for _ in iterable:
        count += 1

    return count
