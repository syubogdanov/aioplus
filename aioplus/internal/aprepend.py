from collections.abc import AsyncIterable, AsyncIterator
from dataclasses import dataclass
from typing import TypeVar

from aioplus.internal.utils.abc import AioplusIterator


T = TypeVar("T")
V = TypeVar("V")


def aprepend(value: V, aiterable: AsyncIterable[T], /) -> AsyncIterator[V | T]:
    """Yield ``value``, then from ``aiterable``.

    Parameters
    ----------
    value : V
        Value.

    aiterable : AsyncIterable[T]
        Iterable.

    Returns
    -------
    AsyncIterator[V | T]
        Iterator.

    Examples
    --------
    >>> [num async for num in aprepend(0, arange(1, 5))]
    [0, 1, 2, 3, 4]
    """
    if not isinstance(aiterable, AsyncIterable):
        detail = "'aiterable' must be 'AsyncIterable'"
        raise TypeError(detail)

    aiterator = aiter(aiterable)
    return AprependIterator(value, aiterator)


@dataclass(repr=False)
class AprependIterator(AioplusIterator[V | T]):
    """An asynchronous iterator."""

    value: V
    aiterator: AsyncIterator[T]

    def __post_init__(self) -> None:
        """Initialize the object."""
        self._started_flg: bool = False

    async def __aioplus__(self) -> V | T:
        """Return the next item."""
        if not self._started_flg:
            self._started_flg = True
            return self.value

        return await anext(self.aiterator)
