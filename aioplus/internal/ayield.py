import asyncio


async def ayield() -> None:
    """Yield control to the event loop."""
    await asyncio.sleep(0)
