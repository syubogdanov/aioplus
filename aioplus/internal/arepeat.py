from collections.abc import AsyncIterator
from dataclasses import dataclass
from typing import TypeVar

from aioplus.internal.utils.abc import AioplusIterator


T = TypeVar("T")


def arepeat(obj: T, /, *, times: int | None = None) -> AsyncIterator[T]:
    """Return the same object repeatedly.

    Parameters
    ----------
    obj : T
        Object.

    times : int, optional
        Count.

    Returns
    -------
    AsyncIterator[T]
        Iterator.

    Notes
    -----
    * If ``times`` is :obj:`None`, then the iterable will be infinite.

    Examples
    --------
    >>> [num async for num in arepeat(23, times=4)]
    [23, 23, 23, 23]

    See Also
    --------
    :func:`itertools.repeat`
    """
    if times is not None and not isinstance(times, int):
        detail = "'times' must be 'int' or 'None'"
        raise TypeError(detail)

    if times is not None and times < 0:
        detail = "'times' must be non-negative"
        raise ValueError(detail)

    return ArepeatIterator(obj, times)


@dataclass(repr=False)
class ArepeatIterator(AioplusIterator[T]):
    """An asynchronous iterator."""

    obj: T
    times: int | None

    def __post_init__(self) -> None:
        """Initialize the object."""
        self._count: int = 0

    async def __aioplus__(self) -> T:
        """Return the next item."""
        if self.times is None:
            return self.obj

        if self._count >= self.times:
            raise StopAsyncIteration

        self._count += 1
        return self.obj
