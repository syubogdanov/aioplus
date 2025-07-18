from asyncio import get_running_loop
from collections.abc import Awaitable, Callable
from concurrent.futures import Executor
from contextvars import copy_context
from dataclasses import dataclass
from functools import partial
from typing import ParamSpec, TypeVar


ReturnT = TypeVar("ReturnT")
ParamsT = ParamSpec("ParamsT")


@dataclass
class Awaitifier:
    """An awaitifier."""

    executor: Executor | None = None

    def awaitify(
        self,
        func: Callable[ParamsT, ReturnT],
        /,
    ) -> Callable[ParamsT, Awaitable[ReturnT]]:
        """Make function `func` asynchronous."""
        return lambda *args, **kwargs: self._to_executor(func, *args, **kwargs)

    async def _to_executor(
        self,
        func: Callable[ParamsT, ReturnT],
        /,
        *args: ParamsT.args,
        **kwargs: ParamsT.kwargs,
    ) -> ReturnT:
        loop = get_running_loop()
        context = copy_context()
        execute = partial(context.run, func, *args, **kwargs)
        return await loop.run_in_executor(self.executor, execute)
