from collections.abc import Awaitable, Callable
from concurrent.futures import Executor
from typing import ParamSpec, TypeVar

from aioplus.internal.awaitifier import Awaitifier


T = TypeVar("T")

ReturnT = TypeVar("ReturnT")
ParamsT = ParamSpec("ParamsT")


def awaitify(
    func: Callable[ParamsT, ReturnT],
    /,
    *,
    executor: Executor | None = None,
) -> Callable[ParamsT, Awaitable[ReturnT]]:
    """Make function `func` asynchronous."""
    awaitifier = Awaitifier(executor)
    return awaitifier.awaitify(func)
