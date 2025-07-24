from collections.abc import AsyncIterable


async def aany(aiterable: AsyncIterable[object], /) -> bool:
    """Return `True` if any element of the iterable.

    Notes
    -----
    * If the iterable is empty, returns `False`.
    """
    async for value in aiterable:
        if value:
            return True
    return False
