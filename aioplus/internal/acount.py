import asyncio

from collections.abc import AsyncIterable, AsyncIterator
from dataclasses import dataclass
from typing import Self, SupportsIndex

from aioplus.internal.coercions import to_int


def acount(
    start: SupportsIndex = 0,
    step: SupportsIndex = 1,
) -> AsyncIterable[int]:
    """Return evenly spaced values beginning with ``start``.

    Parameters
    ----------
    start : int, default 0
        The initial value. Must be an object supporting :meth:`object.__index__`.

    step : int, default 1
        The difference between consecutive values. Must be an object supporting
        :meth:`object.__index__`.

    Returns
    -------
    AsyncIterable of int
        An infinite asynchronous iterable yielding integers, starting from ``start``
        and incremented by ``step``.

    Examples
    --------
    >>> [num async for num in acount(start=23, step=4)]
    [23, 27, 31, 35, 39, 43, 47, ...]

    Notes
    -----
    - Yields control to the event loop before producing each value.

    See Also
    --------
    :func:`itertools.count`
    """
    start = to_int(start, variable_name="start")
    step = to_int(step, variable_name="step")

    return AcountIterable(start, step)


@dataclass
class AcountIterable(AsyncIterable[int]):
    """An asynchronous iterable."""

    start: int
    step: int

    def __aiter__(self) -> AsyncIterator[int]:
        """Return an asynchronous iterator."""
        return AcountIterator(self.start, self.step)


@dataclass
class AcountIterator(AsyncIterator[int]):
    """An asynchronous iterator."""

    start: int
    step: int

    def __post_init__(self) -> None:
        """Initialize the object."""
        self._next_value = self.start

    def __aiter__(self) -> Self:
        """Return an asynchronous iterator."""
        return self

    async def __anext__(self) -> int:
        """Return the next value."""
        value = self._next_value
        self._next_value += self.step

        # Move to the next coroutine!
        await asyncio.sleep(0.0)

        return value
