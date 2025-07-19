import asyncio

from asyncio import Future, Task
from collections.abc import Iterable
from typing import TypeVar, overload


T = TypeVar("T")


@overload
async def afirst(
    awaitables: Iterable[Task[T]],
    /,
    *,
    timeout: float | None = None,
) -> tuple[set[Task[T]], set[Task[T]]]: ...


@overload
async def afirst(
    awaitables: Iterable[Future[T]],
    /,
    *,
    timeout: float | None = None,
) -> tuple[set[Future[T]], set[Future[T]]]: ...


async def afirst(
    awaitables: Iterable[Task[T] | Future[T]],
    /,
    *,
    timeout: float | None = None,
) -> tuple[set[Task[T] | Future[T]], set[Task[T] | Future[T]]]:
    """Run `Future` and `Task` instances concurrently and block until the first one completes.

    See Also
    --------
    * `asyncio.wait(..., return_when=asyncio.FIRST_COMPLETED)`.
    """
    return await asyncio.wait(awaitables, timeout=timeout, return_when=asyncio.FIRST_COMPLETED)
