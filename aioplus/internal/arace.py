import asyncio

from asyncio import FIRST_COMPLETED, Task, create_task
from collections.abc import AsyncIterable, AsyncIterator
from dataclasses import dataclass
from typing import TYPE_CHECKING, Self, TypeVar, overload


if TYPE_CHECKING:
    from types import EllipsisType


T = TypeVar("T")

T1 = TypeVar("T1")
T2 = TypeVar("T2")
T3 = TypeVar("T3")
T4 = TypeVar("T4")
T5 = TypeVar("T5")
T6 = TypeVar("T6")


@overload
def arace(aiterable: AsyncIterable[T], /) -> AsyncIterable[T]: ...


@overload
def arace(
    aiterable1: AsyncIterable[T1],
    aiterable2: AsyncIterable[T2],
    /,
) -> AsyncIterable[T1 | T2]: ...


@overload
def arace(
    aiterable1: AsyncIterable[T1],
    aiterable2: AsyncIterable[T2],
    aiterable3: AsyncIterable[T3],
    /,
) -> AsyncIterable[T1 | T2 | T3]: ...


@overload
def arace(
    aiterable1: AsyncIterable[T1],
    aiterable2: AsyncIterable[T2],
    aiterable3: AsyncIterable[T3],
    aiterable4: AsyncIterable[T4],
    /,
) -> AsyncIterable[T1 | T2 | T3 | T4]: ...


@overload
def arace(
    aiterable1: AsyncIterable[T1],
    aiterable2: AsyncIterable[T2],
    aiterable3: AsyncIterable[T3],
    aiterable4: AsyncIterable[T4],
    aiterable5: AsyncIterable[T5],
    /,
) -> AsyncIterable[T1 | T2 | T3 | T4 | T5]: ...


@overload
def arace(
    aiterable1: AsyncIterable[T1],
    aiterable2: AsyncIterable[T2],
    aiterable3: AsyncIterable[T3],
    aiterable4: AsyncIterable[T4],
    aiterable5: AsyncIterable[T5],
    aiterable6: AsyncIterable[T6],
    /,
) -> AsyncIterable[T1 | T2 | T3 | T4 | T5 | T6]: ...


@overload
def arace(*aiterables: AsyncIterable[T]) -> AsyncIterable[T]: ...


def arace(*aiterables: AsyncIterable[T]) -> AsyncIterable[T]:
    """Iterate ``*aiterables``, returning values as they become available.

    Parameters
    ----------
    *aiterables : AsyncIterable[T]
        The asynchronous iterables.

    Returns
    -------
    AsyncIterable[tuple[T, ...]]
        The asynchronous iterable.

    Examples
    --------
    >>> nums1 = arange(0, 3)
    >>> nums2 = arange(3, 6)
    >>> nums3 = arange(6, 9)
    >>> [num async for num in arace(nums1, nums2, nums3)]
    [0, 6, 3, 1, 4, 7, 5, 2, 8]
    """
    if not aiterables:
        detail = "'*aiterables' must be non-empty"
        raise ValueError(detail)

    for aiterable in aiterables:
        if not isinstance(aiterable, AsyncIterable):
            detail = "'*aiterables' must be 'AsyncIterable'"
            raise TypeError(detail)

    return AraceIterable(aiterables)


@dataclass(repr=False)
class AraceIterable(AsyncIterable[T]):
    """An asynchronous iterable."""

    aiterables: tuple[AsyncIterable[T], ...]

    def __aiter__(self) -> AsyncIterator[T]:
        """Return an asynchronous iterator."""
        aiterators = [aiter(aiterable) for aiterable in self.aiterables]
        return AraceIterator(aiterators)


@dataclass(repr=False)
class AraceIterator(AsyncIterator[T]):
    """An asynchronous iterator."""

    aiterators: list[AsyncIterator[T]]

    def __post_init__(self) -> None:
        """Initialize the object."""
        self._started_flg: bool = False
        self._tasks: dict[Task[T | EllipsisType], int] = {}

    def __aiter__(self) -> Self:
        """Return an asynchronous iterator."""
        return self

    async def __anext__(self) -> T:  # noqa: C901
        """Return the next value."""
        if not self._started_flg:
            self._started_flg = True
            for serial, aiterator in enumerate(self.aiterators):
                coroutine = anext(aiterator, ...)
                task = create_task(coroutine)
                self._tasks[task] = serial

        if not self._tasks:
            self._finished_flg = True
            raise StopAsyncIteration

        exceptions: list[Exception] = []
        base_exceptions: list[BaseException] = []

        for _ in range(len(self._tasks)):
            done, _ = await asyncio.wait(self._tasks, return_when=FIRST_COMPLETED)

            task = done.pop()
            index = self._tasks.pop(task)

            try:
                maybe_result = task.result()

            except ExceptionGroup as group:
                exceptions.extend(group.exceptions)
            except BaseExceptionGroup as group:
                base_exceptions.extend(group.exceptions)

            except Exception as exception:
                exceptions.append(exception)
            except BaseException as exception:
                base_exceptions.append(exception)

            else:
                if not base_exceptions and not exceptions and maybe_result is not ...:
                    aiterator = self.aiterators[index]
                    coroutine = anext(aiterator, ...)
                    task = create_task(coroutine)
                    self._tasks[task] = index
                    return maybe_result

        if base_exceptions:
            detail = "azip(): base exception(-s) occurred"
            raise BaseExceptionGroup(detail, [*base_exceptions, *exceptions])

        if exceptions:
            detail = "azip(): exception(-s) occurred"
            raise ExceptionGroup(detail, exceptions)

        raise StopAsyncIteration
