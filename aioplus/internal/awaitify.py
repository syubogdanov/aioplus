from asyncio import get_running_loop
from collections.abc import Awaitable, Callable
from concurrent.futures import ThreadPoolExecutor
from contextvars import copy_context
from functools import partial, wraps
from typing import ParamSpec, TypeVar


ReturnT = TypeVar("ReturnT")
ParamsT = ParamSpec("ParamsT")


def awaitify(
    func: Callable[ParamsT, ReturnT],
    /,
    *,
    executor: ThreadPoolExecutor | None = None,
) -> Callable[ParamsT, Awaitable[ReturnT]]:
    """Make a function asynchronous.

    Parameters
    ----------
    func : Callable
        A callable to be wrapped for asynchronous execution.

    executor : ThreadPoolExecutor, optional
        An optional :class:`concurrent.futures.ThreadPoolExecutor` to run the function in. If
        :obj:`None`, the default executor is used.

    Returns
    -------
    Callable
        An asynchronous callable that, when awaited, runs the original function in the executor.

    Examples
    --------
    >>> aprint = awaitify(print)
    >>> await aprint("4 -> 23")
    4 -> 23

    See Also
    --------
    :meth:`asyncio.loop.run_in_executor`
    """
    if not callable(func):
        detail = "'func' must be 'Callable'"
        raise TypeError(detail)

    if executor is not None and not isinstance(executor, ThreadPoolExecutor):
        detail = "'executor' must be 'ThreadPoolExecutor' or 'None'"
        raise TypeError(detail)

    @wraps(func)
    async def afunc(*args: ParamsT.args, **kwargs: ParamsT.kwargs) -> ReturnT:
        """Run the function asynchronously."""
        loop = get_running_loop()
        context = copy_context()
        execute = partial(context.run, func, *args, **kwargs)
        return await loop.run_in_executor(executor, execute)

    return afunc
