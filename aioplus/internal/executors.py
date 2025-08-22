from collections.abc import Callable
from concurrent.futures import Executor, Future
from typing import ParamSpec, TypeVar

from aioplus.internal import coercions


P = ParamSpec("P")
R = TypeVar("R")


class CallerThreadExecutor(Executor):
    """An executor that uses the caller thread.

    Examples
    --------
    >>> executor = CallerThreadExecutor()
    >>> iterable = [1, 2, 3, 4, 5, 6, 7, 8]
    >>> aiterable = anextify(iterable, executor=executor)
    >>> [num async for num in aiterable]
    [1, 2, 3, 4, 5, 6, 7, 8]

    See Also
    --------
    :class:`concurrent.futures.Executor`
    """

    def submit(self, fn: Callable[P, R], /, *args: P.args, **kwargs: P.kwargs) -> Future[R]:
        """Schedule the callable, ``fn``, to be executed.

        Parameters
        ----------
        fn : Callable[P, R]
            The callable to be executed.

        *args : P.args
            Positional arguments to pass to the callable.

        **kwargs : P.kwargs
            Keyword arguments to pass to the callable.

        Returns
        -------
        Future[R]
            A Future representing the execution of the callable.

        Notes
        -----
        * Tasks are executed immediately (not lazy) to avoid deferred execution in destructors.
        """
        fn = coercions.be_callable(fn, variable_name="fn")

        future: Future[R] = Future()

        try:
            result = fn(*args, **kwargs)
            future.set_result(result)

        except Exception as exception:
            future.set_exception(exception)

        return future
