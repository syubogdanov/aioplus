from collections.abc import AsyncIterable, AsyncIterator
from dataclasses import dataclass
from typing import Self, TypeVar


T = TypeVar("T")
V = TypeVar("V")


def aprepend(value: V, aiterable: AsyncIterable[T], /) -> AsyncIterator[V | T]:
    """Yield ``value``, followed by elements in ``aiterable``.

    Parameters
    ----------
    value : V
        The value.

    aiterable : AsyncIterable[T]
        The asynchronous iterable.

    Returns
    -------
    AsyncIterator[V | T]
        The asynchronous iterator.

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
class AprependIterator(AsyncIterator[V | T]):
    """An asynchronous iterator."""

    value: V
    aiterator: AsyncIterator[T]

    def __post_init__(self) -> None:
        """Initialize the object."""
        self._started_flg: bool = False
        self._finished_flg: bool = False

    def __aiter__(self) -> Self:
        """Return an asynchronous iterator."""
        return self

    async def __anext__(self) -> V | T:
        """Return the next item."""
        if self._finished_flg:
            raise StopAsyncIteration

        if not self._started_flg:
            self._started_flg = True
            return self.value

        try:
            item = await anext(self.aiterator)

        except (StopAsyncIteration, BaseException):
            self._finished_flg = True
            raise

        return item
