import asyncio

from abc import ABC, abstractmethod
from asyncio import CancelledError, Lock
from collections.abc import AsyncIterator
from typing import Self, TypeVar


T = TypeVar("T")


class AioplusIterator(ABC, AsyncIterator[T]):
    """An asynchronous iterator."""

    __slots__: tuple[str, ...] = (
        "_aioplus_cancelled_flg",
        "_aioplus_exception_flg",
        "_aioplus_finished_flg",
        "_aioplus_lock",
    )

    def __aiter__(self) -> Self:
        """Return self."""
        return self

    async def __anext__(self) -> T:
        """Return the next item."""
        if not hasattr(self, "_aioplus_lock"):
            self._aioplus_lock = Lock()

        async with self._aioplus_lock:
            if getattr(self, "_aioplus_cancelled_flg", False):
                detail = "cannot iterate after cancellation"
                raise StopAsyncIteration(detail)

            if getattr(self, "_aioplus_exception_flg", False):
                detail = "cannot iterate after exception(-s)"
                raise StopAsyncIteration(detail)

            if getattr(self, "_aioplus_finished_flg", False):
                detail = "cannot iterate after exhausting"
                raise StopAsyncIteration(detail)

            try:
                # Move to the next task!
                await asyncio.sleep(0.0)

                item = await self.__aioplus__()

            except StopAsyncIteration:
                self._aioplus_finished_flg = True
                raise

            except CancelledError:
                self._aioplus_cancelled_flg = True
                raise

            except BaseException:
                self._aioplus_exception_flg = True
                raise

        return item

    @abstractmethod
    async def __aioplus__(self) -> T:
        """Return the next item."""
