from collections.abc import AsyncIterable, AsyncIterator
from dataclasses import dataclass
from typing import Self, TypeVar

from aioplus.internal.aislice import aislice


T = TypeVar("T")


def abatched(
    iterable: AsyncIterable[T],
    /,
    *,
    n: int,
    strict: bool = False,
) -> AsyncIterable[tuple[T, ...]]:
    """Batch data from the `iterable` into tuples of length `n`."""
    if not isinstance(iterable, AsyncIterable):
        detail = "'iterable' must be 'AsyncIterable'"
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

    return AbatchedIterable(iterable, n, strict)


@dataclass
class AbatchedIterable(AsyncIterable[tuple[T, ...]]):
    """An iterable that batches data."""

    iterable: AsyncIterable[T]
    n: int
    strict: bool

    def __aiter__(self) -> AsyncIterator[tuple[T, ...]]:
        """Return an asynchronous iterator."""
        iterator = aiter(self.iterable)
        return AbatchedIterator(iterator, self.n, self.strict)


@dataclass
class AbatchedIterator(AsyncIterator[tuple[T, ...]]):
    """An iterator that batches data."""

    iterator: AsyncIterator[T]
    n: int
    strict: bool

    def __aiter__(self) -> Self:
        """Return an asynchronous iterator."""
        return self

    async def __anext__(self) -> tuple[T, ...]:
        """Return the next value."""
        batch = [value async for value in aislice(self.iterator, self.n)]

        if not batch:
            raise StopAsyncIteration

        if len(batch) < self.n and self.strict:
            detail = "abatched(): incomplete batch"
            raise ValueError(detail)

        return tuple(batch)
