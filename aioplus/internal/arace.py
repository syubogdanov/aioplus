import asyncio

from asyncio import FIRST_COMPLETED, Task, create_task
from collections.abc import AsyncIterable, AsyncIterator
from dataclasses import dataclass
from typing import TYPE_CHECKING, Self, TypeVar, overload
from warnings import warn

from aioplus.internal.utils.typing import AcloseableIterator


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
def arace(aiterable: AsyncIterable[T], /) -> AcloseableIterator[T]: ...


@overload
def arace(
    aiterable1: AsyncIterable[T1],
    aiterable2: AsyncIterable[T2],
    /,
) -> AcloseableIterator[T1 | T2]: ...


@overload
def arace(
    aiterable1: AsyncIterable[T1],
    aiterable2: AsyncIterable[T2],
    aiterable3: AsyncIterable[T3],
    /,
) -> AcloseableIterator[T1 | T2 | T3]: ...


@overload
def arace(
    aiterable1: AsyncIterable[T1],
    aiterable2: AsyncIterable[T2],
    aiterable3: AsyncIterable[T3],
    aiterable4: AsyncIterable[T4],
    /,
) -> AcloseableIterator[T1 | T2 | T3 | T4]: ...


@overload
def arace(
    aiterable1: AsyncIterable[T1],
    aiterable2: AsyncIterable[T2],
    aiterable3: AsyncIterable[T3],
    aiterable4: AsyncIterable[T4],
    aiterable5: AsyncIterable[T5],
    /,
) -> AcloseableIterator[T1 | T2 | T3 | T4 | T5]: ...


@overload
def arace(
    aiterable1: AsyncIterable[T1],
    aiterable2: AsyncIterable[T2],
    aiterable3: AsyncIterable[T3],
    aiterable4: AsyncIterable[T4],
    aiterable5: AsyncIterable[T5],
    aiterable6: AsyncIterable[T6],
    /,
) -> AcloseableIterator[T1 | T2 | T3 | T4 | T5 | T6]: ...


@overload
def arace(*aiterables: AsyncIterable[T]) -> AcloseableIterator[T]: ...


def arace(*aiterables: AsyncIterable[T]) -> AcloseableIterator[T]:
    """Iterate ``*aiterables``, returning values as they become available.

    Parameters
    ----------
    *aiterables : AsyncIterable[T]
        The asynchronous iterables.

    Returns
    -------
    AsyncIterator[T]
        The asynchronous iterator.

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

    aiterators = [aiter(aiterable) for aiterable in aiterables]
    return AraceIterator(aiterators)


@dataclass(repr=False)
class AraceIterator(AsyncIterator[T]):
    """An asynchronous iterator."""

    aiterators: list[AsyncIterator[T]]

    def __post_init__(self) -> None:
        """Initialize the object."""
        self._started_flg: bool = False
        self._pending: dict[Task[T | EllipsisType], int] = {}
        self._done: dict[Task[T | EllipsisType], int] = {}

    def __aiter__(self) -> Self:
        """Return an asynchronous iterator."""
        return self

    async def __anext__(self) -> T:
        """Return the next value."""
        if not self._started_flg:
            self._started_flg = True
            self._schedule_all()

        if not (count := len(self._pending) + len(self._done)):
            raise StopAsyncIteration

        exceptions: list[Exception] = []
        base_exceptions: list[BaseException] = []

        for _ in range(count):
            if (base_exceptions or exceptions) and self._pending:
                self._cancel_all()
                await self._wait_all()

            if not self._done:
                await self._wait_once()

            task, index = self._done.popitem()
            if task.cancelled():
                continue

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
                if not base_exceptions and not exceptions and (maybe_result is not ...):
                    self._schedule_once(index)
                    return maybe_result

        if base_exceptions:
            detail = "arace(): base exception(-s) occurred"
            raise BaseExceptionGroup(detail, [*base_exceptions, *exceptions])

        if exceptions:
            detail = "arace(): exception(-s) occurred"
            raise ExceptionGroup(detail, exceptions)

        raise StopAsyncIteration

    def __del__(self) -> None:
        """Call the destructor."""
        self.close()

    async def aclose(self) -> None:
        """Close the iterator."""
        if self._pending:
            self._cancel_all()
            await self._wait_all()

        self.close()

    def close(self) -> None:
        """Close the iterator."""
        for task in list(self._pending):
            if task.done():
                index = self._pending.pop(task)
                self._done[task] = index

        if tasks := list(self._pending):
            detail = f"arace.close(): task(-s) will never be awaited: {tasks!r}"
            warn(detail, RuntimeWarning, stacklevel=2)

        base_exceptions: list[BaseException] = []

        while self._done:
            task, _ = self._done.popitem()
            try:
                if not task.cancelled():
                    task.result()

            except BaseExceptionGroup as group:
                base_exceptions.extend(group.exceptions)
            except BaseException as exception:
                base_exceptions.append(exception)

        if base_exceptions:
            detail = f"arace.close(): base exception(-s) occurred: {base_exceptions!r}"
            warn(detail, RuntimeWarning, stacklevel=2)

        self._pending.clear()
        self._done.clear()

    def _cancel_all(self) -> None:
        """Cancel all pending tasks."""
        for task in self._pending:
            if not task.done():
                task.cancel()

    def _schedule_once(self, index: int, /) -> None:
        """Schedule the asynchronous iterator."""
        aiterator = self.aiterators[index]
        coroutine = anext(aiterator, ...)
        task = create_task(coroutine)
        self._pending[task] = index

    def _schedule_all(self) -> None:
        """Schedule all asynchronous iterators."""
        count = len(self.aiterators)
        for index in range(count):
            self._schedule_once(index)

    async def _wait_all(self) -> None:
        """Wait until all tasks are done."""
        if self._pending:
            done, _ = await asyncio.wait(self._pending)
            for task in done:
                index = self._pending.pop(task)
                self._done[task] = index

    async def _wait_once(self) -> None:
        """Wait until at least one task is done."""
        if self._pending:
            done, _ = await asyncio.wait(self._pending, return_when=FIRST_COMPLETED)
            for task in done:
                index = self._pending.pop(task)
                self._done[task] = index
