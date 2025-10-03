from asyncio import iscoroutinefunction
from collections.abc import AsyncIterable, AsyncIterator, Awaitable, Callable
from dataclasses import dataclass
from typing import Self, TypeVar


R = TypeVar("R")


def atabulate(func: Callable[[int], Awaitable[R]], /, *, start: int = 0) -> AsyncIterable[R]:
    """Return ``await func(0)``, ``await func(1)``, etc.

    Parameters
    ----------
    func : Callable[[int], Awaitable[R]]
        The function to be applied.

    Returns
    -------
    AsyncIterable[R]
        An asynchronous iterable.

    Examples
    --------
    >>> afunc = awaitify(lambda x: x * x)
    >>> [num async for num in atabulate(afunc)]
    [0, 1, 4, 9, 16, 25, 36, 49, ...]
    """
    if not callable(func):
        detail = "'func' must be 'Callable'"
        raise TypeError(detail)

    if not iscoroutinefunction(func):
        detail = "'func' must be a coroutine function"
        raise TypeError(detail)

    if not isinstance(start, int):
        detail = "'start' must be 'int'"
        raise TypeError(detail)

    return AtabulateIterable(func, start)


@dataclass
class AtabulateIterable(AsyncIterable[R]):
    """An asynchronous iterable."""

    func: Callable[[int], Awaitable[R]]
    start: int

    def __aiter__(self) -> AsyncIterator[R]:
        """Return an asynchronous iterator."""
        return AtabulateIterator(self.func, self.start)


@dataclass
class AtabulateIterator(AsyncIterator[R]):
    """An asynchronous iterator."""

    func: Callable[[int], Awaitable[R]]
    next: int

    def __post_init__(self) -> None:
        """Initialize the object."""
        self._finished_flg: bool = False

    def __aiter__(self) -> Self:
        """Return an asynchronous iterator."""
        return self

    async def __anext__(self) -> R:
        """Return the next value."""
        if self._finished_flg:
            raise StopAsyncIteration

        try:
            value = await self.func(self.next)

        except Exception:
            self._finished_flg = True
            raise

        self.next += 1
        return value
