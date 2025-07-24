from collections.abc import AsyncIterable, AsyncIterator
from dataclasses import dataclass
from typing import Self, TypeVar

from aioplus.internal.aislice import aislice


T = TypeVar("T")


def abatched(
    aiterable: AsyncIterable[T],
    /,
    *,
    n: int,
    strict: bool = False,
) -> AsyncIterable[tuple[T, ...]]:
    """Batch data from the `aiterable` into tuples of length `n`."""
    if not isinstance(aiterable, AsyncIterable):
        detail = "'aiterable' must be 'AsyncIterable'"
        raise TypeError(detail)

    if not isinstance(n, int):
        detail = "'n' must be 'int'"
        raise TypeError(detail)

    if n < 1:
        detail = "'n' must be at least one"
        raise ValueError(detail)

    if not isinstance(strict, bool):
        detail = "'strict' must be 'bool'"
        raise TypeError(detail)

    return AbatchedIterable(aiterable, n, strict)


@dataclass
class AbatchedIterable(AsyncIterable[tuple[T, ...]]):
    """An asynchronous iterable that batches data."""

    aiterable: AsyncIterable[T]
    n: int
    strict: bool

    def __aiter__(self) -> AsyncIterator[tuple[T, ...]]:
        """Return an asynchronous iterator."""
        aiterator = aiter(self.aiterable)
        return AbatchedIterator(aiterator, self.n, self.strict)


@dataclass
class AbatchedIterator(AsyncIterator[tuple[T, ...]]):
    """An asynchronous iterator that batches data."""

    aiterator: AsyncIterator[T]
    n: int
    strict: bool

    def __post_init__(self) -> None:
        """Initialize the object."""
        self._finished_flg: bool = False

    def __aiter__(self) -> Self:
        """Return an asynchronous iterator."""
        return self

    async def __anext__(self) -> tuple[T, ...]:
        """Return the next value."""
        if self._finished_flg:
            raise StopAsyncIteration

        batch = [value async for value in aislice(self.aiterator, self.n)]

        if not batch:
            self._finished_flg = True
            raise StopAsyncIteration

        if len(batch) < self.n and self.strict:
            self._finished_flg = True
            detail = "abatched(): incomplete batch"
            raise ValueError(detail)

        return tuple(batch)
