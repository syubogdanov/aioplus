from asyncio import iscoroutinefunction
from collections.abc import AsyncIterable, AsyncIterator, Awaitable, Callable
from dataclasses import dataclass
from typing import Self, TypeVar


R = TypeVar("R")


def atabulate(afunc: Callable[[int], Awaitable[R]], /, *, start: int = 0) -> AsyncIterable[R]:
    """Return ``await afunc(0)``, ``await afunc(1)``, ``await afunc(2)``, etc.

    Parameters
    ----------
    afunc : Callable[[int], Awaitable[R]]
        The callable.

    Returns
    -------
    AsyncIterable[R]
        The asynchronous iterable.

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

    return AtabulateIterable(afunc, start)


@dataclass(repr=False)
class AtabulateIterable(AsyncIterable[R]):
    """An asynchronous iterable."""

    afunc: Callable[[int], Awaitable[R]]
    start: int

    def __aiter__(self) -> AsyncIterator[R]:
        """Return an asynchronous iterator."""
        return AtabulateIterator(self.afunc, self.start)


@dataclass(repr=False)
class AtabulateIterator(AsyncIterator[R]):
    """An asynchronous iterator."""

    afunc: Callable[[int], Awaitable[R]]
    next: int

    def __post_init__(self) -> None:
        """Initialize the object."""
        self._finished_flg: bool = False

    def __aiter__(self) -> Self:
        """Return an asynchronous iterator."""
        return self

    async def __anext__(self) -> R:
        """Return the next item."""
        if self._finished_flg:
            raise StopAsyncIteration

        try:
            item = await self.afunc(self.next)

        except BaseException:
            self._finished_flg = True
            raise

        self.next += 1
        return item
