import asyncio


async def ayield() -> None:
    """Yield control to the event loop.

    See Also
    --------
    * `asyncio.sleep(0)`.
    """
    await asyncio.sleep(0)
