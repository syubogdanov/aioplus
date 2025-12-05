from collections.abc import AsyncIterator
from dataclasses import dataclass
from types import EllipsisType
from typing import overload

from aioplus.internal.utils.abc import AioplusIterator


@overload
def arange(stop: int, /) -> AsyncIterator[int]: ...


@overload
def arange(start: int, stop: int, /) -> AsyncIterator[int]: ...


@overload
def arange(start: int, stop: int, step: int, /) -> AsyncIterator[int]: ...


def arange(
    start: int,
    stop: int | EllipsisType = ...,
    step: int | EllipsisType = ...,
    /,
) -> AsyncIterator[int]:
    """Return a sequence of numbers.

    Parameters
    ----------
    start : int
        Start.

    stop : int, unset
        Stop.

    step : int, unset
        Step.

    Returns
    -------
    AsyncIterator[int]
        Iterator.

    Examples
    --------
    >>> [num async for num in arange(23)]
    [0, 1, 2, 3, 4, ..., 19, 20, 21, 22]

    See Also
    --------
    :func:`range`
    """
    if not isinstance(start, int):
        detail = "'start' must be 'int'"
        raise TypeError(detail)

    if (stop is not ...) and not isinstance(stop, int):
        detail = "'stop' must be 'int'"
        raise TypeError(detail)

    if (step is not ...) and not isinstance(step, int):
        detail = "'step' must be 'int'"
        raise TypeError(detail)

    if (stop is ...) and (step is not ...):
        detail = "'stop' must be 'int'"
        raise ValueError(detail)

    if stop is ...:
        stop = start
        start = 0
        step = 1

    if step is ...:
        step = 1

    if not step:
        detail = "'step' must not be zero"
        raise ValueError(detail)

    return ArangeIterator(start, stop, step)


@dataclass(repr=False)
class ArangeIterator(AioplusIterator[int]):
    """An asynchronous iterator."""

    start: int
    stop: int
    step: int

    def __post_init__(self) -> None:
        """Initialize the object."""
        self._next = self.start

    async def __aioplus__(self) -> int:
        """Return the next item."""
        if self.step > 0 and self._next >= self.stop:
            raise StopAsyncIteration

        if self.step < 0 and self._next <= self.stop:
            raise StopAsyncIteration

        value = self._next
        self._next += self.step

        return value
