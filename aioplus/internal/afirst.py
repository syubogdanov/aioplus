import asyncio

from asyncio import Future, Task
from collections.abc import Iterable
from typing import TypeVar, overload


T = TypeVar("T")


@overload
async def afirst(
    awaitables: Iterable[Task[T]],
    /,
) -> tuple[Task[T], set[Task[T]]]: ...


@overload
async def afirst(
    awaitables: Iterable[Future[T]],
    /,
) -> tuple[Future[T], set[Future[T]]]: ...


async def afirst(
    awaitables: Iterable[Task[T] | Future[T]],
    /,
) -> tuple[Task[T] | Future[T], set[Task[T] | Future[T]]]:
    """Run `Future` and `Task` instances concurrently and block until the first one completes.

    See Also
    --------
    * `asyncio.wait(..., return_when=asyncio.FIRST_COMPLETED)`.
    """
    done, pending = await asyncio.wait(awaitables, return_when=asyncio.FIRST_COMPLETED)
    return done.pop(), pending
