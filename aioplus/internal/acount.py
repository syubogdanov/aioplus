import asyncio

from collections.abc import AsyncIterator
from dataclasses import dataclass
from typing import Self


def acount(start: int = 0, step: int = 1) -> AsyncIterator[int]:
    """Return evenly spaced integers.

    Parameters
    ----------
    start : int, default 0
        The initial value.

    step : int, default 1
        The difference between consecutives.

    Returns
    -------
    AsyncIterator[int]
        The asynchronous iterator.

    Examples
    --------
    >>> [num async for num in acount(start=23, step=4)]
    [23, 27, 31, 35, 39, 43, 47, ...]

    See Also
    --------
    :func:`itertools.count`
    """
    if not isinstance(start, int):
        detail = "'start' must be 'int'"
        raise TypeError(detail)

    if not isinstance(step, int):
        detail = "'step' must be 'int'"
        raise TypeError(detail)

    return AcountIterator(start, step)


@dataclass(repr=False)
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
        """Return the next item."""
        value = self._next_value
        self._next_value += self.step

        # Move to the next coroutine!
        await asyncio.sleep(0.0)

        return value
