from collections.abc import AsyncIterator
from dataclasses import dataclass

from aioplus.internal.utils.abc import AioplusIterator


def acount(start: int = 0, step: int = 1) -> AsyncIterator[int]:
    """Return evenly spaced integers.

    Parameters
    ----------
    start : int, default 0
        Initializer.

    step : int, default 1
        Step.

    Returns
    -------
    AsyncIterator[int]
        Iterator.

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
class AcountIterator(AioplusIterator[int]):
    """An asynchronous iterator."""

    next: int
    step: int

    async def __aioplus__(self) -> int:
        """Return the next item."""
        item = self.next
        self.next += self.step
        return item
