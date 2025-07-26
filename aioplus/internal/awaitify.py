from asyncio import get_running_loop
from collections.abc import Awaitable, Callable
from concurrent.futures import Executor
from contextvars import copy_context
from functools import partial, wraps
from typing import ParamSpec, TypeVar


ReturnT = TypeVar("ReturnT")
ParamsT = ParamSpec("ParamsT")


def awaitify(
    func: Callable[ParamsT, ReturnT],
    /,
    *,
    executor: Executor | None = None,
) -> Callable[ParamsT, Awaitable[ReturnT]]:
    """Make a function asynchronous.

    Parameters
    ----------
    func : Callable
        A callable to be wrapped for asynchronous execution.

    executor : Executor, optional
        An optional :class:`concurrent.futures.Executor` to run the function in. If :obj:`None`, the
        default executor is used (usually a thread pool).

    Returns
    -------
    Callable
        An asynchronous callable that, when awaited, runs the original function in the executor.

    See Also
    --------
    :func:`asyncio.AbstractEventLoop.run_in_executor`
    """
    if not callable(func):
        detail = "'func' must be callable"
        raise TypeError(detail)

    if executor is not None and not isinstance(executor, Executor):
        detail = "'executor' must be 'Executor' or 'None'"
        raise TypeError(detail)

    @wraps(func)
    async def afunc(*args: ParamsT.args, **kwargs: ParamsT.kwargs) -> ReturnT:
        """Run the function asynchronously."""
        loop = get_running_loop()
        context = copy_context()
        execute = partial(context.run, func, *args, **kwargs)
        return await loop.run_in_executor(executor, execute)

    return afunc
