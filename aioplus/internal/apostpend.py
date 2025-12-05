from collections.abc import AsyncIterable, AsyncIterator
from dataclasses import dataclass
from typing import TypeVar

from aioplus.internal.utils.abc import AioplusIterator


T = TypeVar("T")
V = TypeVar("V")


def apostpend(aiterable: AsyncIterable[T], value: V, /) -> AsyncIterator[T | V]:
    """Yield from ``aiterable``, then ``value``.

    Parameters
    ----------
    aiterable : AsyncIterable[T]
        Iterable.

    value : V
        Value.

    Returns
    -------
    AsyncIterator[T | V]
        Iterator.

    Examples
    --------
    >>> [num async for num in apostpend(arange(4), 4)]
    [0, 1, 2, 3, 4]
    """
    if not isinstance(aiterable, AsyncIterable):
        detail = "'aiterable' must be 'AsyncIterable'"
        raise TypeError(detail)

    aiterator = aiter(aiterable)
    return ApostpendIterator(aiterator, value)


@dataclass(repr=False)
class ApostpendIterator(AioplusIterator[T | V]):
    """An asynchronous iterator."""

    aiterator: AsyncIterator[T]
    value: V

    def __post_init__(self) -> None:
        """Initialize the object."""
        self._finished_flg: bool = False

    async def __aioplus__(self) -> T | V:
        """Return the next item."""
        if self._finished_flg:
            raise StopAsyncIteration

        try:
            item = await anext(self.aiterator)

        except StopAsyncIteration:
            self._finished_flg = True
            return self.value

        return item
