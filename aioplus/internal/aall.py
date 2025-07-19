from collections.abc import AsyncIterable


async def aall(iterable: AsyncIterable[object], /) -> bool:
    """Return `True` if all elements of the iterable are true.

    Notes
    -----
    * If the iterable is empty, returns `True`.
    """
    async for value in iterable:
        if not value:
            return False
    return True
