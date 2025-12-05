from asyncio import iscoroutinefunction
from collections.abc import AsyncIterator, Awaitable, Callable
from dataclasses import dataclass
from typing import TypeVar

from aioplus.internal.utils.abc import AioplusIterator


R = TypeVar("R")


def atabulate(afunc: Callable[[int], Awaitable[R]], /, *, start: int = 0) -> AsyncIterator[R]:
    """Return ``await afunc(0)``, ``await afunc(1)``, ``await afunc(2)``, etc.

    Parameters
    ----------
    afunc : Callable[[int], Awaitable[R]]
        Callable.

    Returns
    -------
    AsyncIterator[R]
        Iterator.

    Examples
    --------
    >>> afunc = awaitify(lambda x: x * x)
    >>> [num async for num in atabulate(afunc)]
    [0, 1, 4, 9, 16, 25, 36, 49, ...]
    """
    if not callable(afunc):
        detail = "'func' must be 'Callable'"
        raise TypeError(detail)

    if not iscoroutinefunction(afunc):
        detail = "'func' must be a coroutine function"
        raise TypeError(detail)

    if not isinstance(start, int):
        detail = "'start' must be 'int'"
        raise TypeError(detail)

    return AtabulateIterator(afunc, start)


@dataclass(repr=False)
class AtabulateIterator(AioplusIterator[R]):
    """An asynchronous iterator."""

    afunc: Callable[[int], Awaitable[R]]
    next: int

    async def __aioplus__(self) -> R:
        """Return the next item."""
        item = await self.afunc(self.next)
        self.next += 1
        return item
