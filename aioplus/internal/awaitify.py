from asyncio import get_running_loop
from collections.abc import Awaitable, Callable
from concurrent.futures import Executor
from contextvars import copy_context
from functools import partial, wraps
from typing import ParamSpec, TypeVar


T = TypeVar("T")

ReturnT = TypeVar("ReturnT")
ParamsT = ParamSpec("ParamsT")


def awaitify(
    func: Callable[ParamsT, ReturnT],
    /,
    *,
    executor: Executor | None = None,
) -> Callable[ParamsT, Awaitable[ReturnT]]:
    """Make function asynchronous."""

    @wraps(func)
    async def afunc(*args: ParamsT.args, **kwargs: ParamsT.kwargs) -> ReturnT:
        """Run the function asynchronously."""
        loop = get_running_loop()
        context = copy_context()
        execute = partial(context.run, func, *args, **kwargs)
        return await loop.run_in_executor(executor, execute)

    return afunc
