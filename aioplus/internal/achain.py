from collections.abc import AsyncIterable, AsyncIterator
from dataclasses import dataclass
from typing import TypeVar, overload

from aioplus.internal.utils.abc import AioplusIterator


T = TypeVar("T")

T1 = TypeVar("T1")
T2 = TypeVar("T2")
T3 = TypeVar("T3")
T4 = TypeVar("T4")
T5 = TypeVar("T5")
T6 = TypeVar("T6")


@overload
def achain(aiterable: AsyncIterable[T], /) -> AsyncIterator[T]: ...


@overload
def achain(
    aiterable1: AsyncIterable[T1],
    aiterable2: AsyncIterable[T2],
    /,
) -> AsyncIterator[T1 | T2]: ...


@overload
def achain(
    aiterable1: AsyncIterable[T1],
    aiterable2: AsyncIterable[T2],
    aiterable3: AsyncIterable[T3],
    /,
) -> AsyncIterator[T1 | T2 | T3]: ...


@overload
def achain(
    aiterable1: AsyncIterable[T1],
    aiterable2: AsyncIterable[T2],
    aiterable3: AsyncIterable[T3],
    aiterable4: AsyncIterable[T4],
    /,
) -> AsyncIterator[T1 | T2 | T3 | T4]: ...


@overload
def achain(
    aiterable1: AsyncIterable[T1],
    aiterable2: AsyncIterable[T2],
    aiterable3: AsyncIterable[T3],
    aiterable4: AsyncIterable[T4],
    aiterable5: AsyncIterable[T5],
    /,
) -> AsyncIterator[T1 | T2 | T3 | T4 | T5]: ...


@overload
def achain(
    aiterable1: AsyncIterable[T1],
    aiterable2: AsyncIterable[T2],
    aiterable3: AsyncIterable[T3],
    aiterable4: AsyncIterable[T4],
    aiterable5: AsyncIterable[T5],
    aiterable6: AsyncIterable[T6],
    /,
) -> AsyncIterator[T1 | T2 | T3 | T4 | T5 | T6]: ...


@overload
def achain(*aiterables: AsyncIterable[T]) -> AsyncIterator[T]: ...


def achain(*aiterables: AsyncIterable[T]) -> AsyncIterator[T]:
    """Iterate ``*aiterables`` sequentially.

    Parameters
    ----------
    *aiterables : AsyncIterable[T]
        Iterables.

    Returns
    -------
    AsyncIterator[T]
        Iterator.

    Examples
    --------
    >>> nums1 = arange(0, 3)
    >>> nums2 = arange(3, 6)
    >>> [num async for num in achain(nums1, nums2)]
    [0, 1, 2, 3, 4, 5]
    """
    if not aiterables:
        detail = "'*aiterables' must be non-empty"
        raise ValueError(detail)

    for aiterable in aiterables:
        if not isinstance(aiterable, AsyncIterable):
            detail = "'*aiterables' must be 'AsyncIterable'"
            raise TypeError(detail)

    aiterators = [aiter(aiterable) for aiterable in aiterables]
    return AchainIterator(aiterators)


@dataclass(repr=False)
class AchainIterator(AioplusIterator[T]):
    """An asynchronous iterator."""

    aiterators: list[AsyncIterator[T]]

    def __post_init__(self) -> None:
        """Initialize the object."""
        self._index = 0

    async def __aioplus__(self) -> T:
        """Return the next item."""
        while self._index < len(self.aiterators):
            aiterator = self.aiterators[self._index]
            try:
                item = await anext(aiterator)

            except StopAsyncIteration:
                self._index += 1
                continue

            return item

        raise StopAsyncIteration
