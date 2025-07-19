from collections.abc import AsyncIterable
from typing import TypeVar, overload


T = TypeVar("T")


@overload
def aislice(iterable: AsyncIterable[T], stop: int, /) -> AsyncIterable[T]: ...


@overload
def aislice(iterable: AsyncIterable[T], start: int, stop: int, /) -> AsyncIterable[T]: ...


@overload
def aislice(
    iterable: AsyncIterable[T],
    start: int,
    stop: int,
    step: int,
    /,
) -> AsyncIterable[T]: ...


def aislice(
    iterable: AsyncIterable[T],
    start: int,
    stop: int | None = None,
    step: int | None = None,
    /,
) -> AsyncIterable[T]:
    """Make an asynchronous iterator that returns selected elements from the iterable."""
    raise NotImplementedError
