import time

from collections.abc import Callable, Iterable, Iterator
from concurrent.futures import Future, ThreadPoolExecutor
from threading import Lock
from types import TracebackType
from typing import Any, Literal, ParamSpec, Self, TypeVar


P = ParamSpec("P")
R = TypeVar("R")


class CallerThreadExecutor(ThreadPoolExecutor):
    """An executor that uses the caller thread.

    Examples
    --------
    >>> executor = CallerThreadExecutor()
    >>> loop = asyncio.new_event_loop()
    >>> loop.set_default_executor(executor)

    See Also
    --------
    :class:`concurrent.futures.ThreadPoolExecutor`
    """

    __slots__ = ("_futures_count", "_futures_lock", "_shutdown", "_shutdown_lock")

    def __init__(
        self,
        max_workers: int | None = None,
        thread_name_prefix: str = "",
        initializer: Callable[..., Any] | None = None,
        initargs: tuple[Any, ...] = (),
    ) -> None:
        """Initialize the object.

        Parameters
        ----------
        max_workers : int or None
            This parameter does not affect the behavior of the executor.

        thread_name_prefix : str
            This parameter does not affect the behavior of the executor.

        initializer : Callable[..., Any] or None
            This parameter does not affect the behavior of the executor.

        initargs : tuple[Any, ...]
            This parameter does not affect the behavior of the executor.

        Notes
        -----
        * Parameters are never used and serve as placeholders to comply with the interface of
          `concurrent.futures.ThreadPoolExecutor` (Liskov Substitution Principle).
        """
        if max_workers is not None and not isinstance(max_workers, int):
            detail = "'max_workers' must be 'int' or 'None'"
            raise TypeError(detail)

        if max_workers is not None and max_workers <= 0:
            detail = "'max_workers' must be positive"
            raise ValueError(detail)

        if not isinstance(thread_name_prefix, str):
            detail = "'thread_name_prefix' must be 'str'"
            raise TypeError(detail)

        if initializer is not None and not callable(initializer):
            detail = "'initializer' must be 'Callable' or 'None'"
            raise TypeError(detail)

        if not isinstance(initargs, tuple):
            detail = "'initargs' must be 'tuple'"
            raise TypeError(detail)

        self._futures_count: int = 0
        self._futures_lock = Lock()
        self._shutdown: bool = False
        self._shutdown_lock = Lock()

    def submit(self, fn: Callable[P, R], /, *args: P.args, **kwargs: P.kwargs) -> Future[R]:
        """Schedules the callable, ``fn``, to be executed.

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
            A future representing the execution of the callable.

        Notes
        -----
        * Submitted tasks are executed immediately.
        """
        if not callable(fn):
            detail = "'fn' must be 'Callable'"
            raise TypeError(detail)

        with self._shutdown_lock:
            if self._shutdown:
                detail = "cannot schedule new futures after shutdown"
                raise RuntimeError(detail)

            future: Future[R] = Future()
            future.set_running_or_notify_cancel()

            with self._futures_lock:
                self._futures_count += 1

        try:
            result = fn(*args, **kwargs)
        except BaseException as exception:
            future.set_exception(exception)
        else:
            future.set_result(result)

        with self._futures_lock:
            self._futures_count -= 1

        return future

    def map(  # noqa: C901
        self,
        fn: Callable[..., R],
        *iterables: Iterable[Any],
        timeout: float | None = None,
        chunksize: int = 1,
        buffersize: int | None = None,
    ) -> Iterator[R]:
        """Map the function to the iterables.

        Parameters
        ----------
        fn : Callable[P, R]
            The function to map.

        *iterables : Iterable[P]
            The iterables to map the function to.

        timeout : float | None
            The timeout for the operation.

        chunksize : int
            This parameter does not affect the behavior of the executor.

        buffersize : int | None
            This parameter does not affect the behavior of the executor.

        Returns
        -------
        Iterator[R]
            An iterator over the results.

        Notes
        -----
        * This method submits lazily to avoid blocking the caller thread on infinite iterators;
        * If ``timeout`` is specified, then :exc:`TimeoutError` is always raised. The executor uses
          the caller thread, so there is no way to enforce the timeout.
        """
        if not callable(fn):
            detail = "'fn' must be 'Callable'"
            raise TypeError(detail)

        for iterable in iterables:
            if not isinstance(iterable, Iterable):
                detail = "'*iterables' must be 'Iterable'"
                raise TypeError(detail)

        if timeout is not None and not isinstance(timeout, float):
            detail = "'timeout' must be 'float' or 'None'"
            raise TypeError(detail)

        if not isinstance(chunksize, int):
            detail = "'chunksize' must be 'int'"
            raise TypeError(detail)

        if chunksize <= 0:
            detail = "'chunksize' must be positive"
            raise ValueError(detail)

        if buffersize is not None and not isinstance(buffersize, int):
            detail = "'buffersize' must be 'int' or 'None'"
            raise TypeError(detail)

        if buffersize is not None and buffersize <= 0:
            detail = "'buffersize' must be positive"
            raise ValueError(detail)

        def iterator() -> Iterator[R]:
            """Iterate over the results."""
            if timeout is not None:
                time.sleep(timeout)
                raise TimeoutError

            for args in zip(*iterables, strict=False):
                future = self.submit(fn, *args)
                yield future.result()

        return iterator()

    def shutdown(
        self,
        wait: bool = True,  # noqa: FBT001, FBT002
        *,
        cancel_futures: bool = False,
    ) -> None:
        """Signal the executor that it should free resources.

        Parameters
        ----------
        wait : bool
            If ``wait`` is :obj:`True` then this method will not return until all the pending
            futures are done executing and the resources associated with the executor have been
            freed. If ``wait`` is :obj:`False` then this method will return immediately and the
            resources associated with the executor will be freed when all pending futures are done
            executing.

        cancel_futures : bool
            This parameter does not affect the behavior of the executor.

        Returns
        -------
        None
            This method does not return a value.
        """
        if not isinstance(wait, bool):
            detail = "'wait' must be 'bool'"
            raise TypeError(detail)

        if not isinstance(cancel_futures, bool):
            detail = "'cancel_futures' must be 'bool'"
            raise TypeError(detail)

        with self._shutdown_lock:
            self._shutdown = True

        if wait:
            while self._futures_count > 0:
                pass  # Just a spin-wait

    def __enter__(self) -> Self:
        """Enter the context.

        Returns
        -------
        Self
            The executor iteself.
        """
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> Literal[False]:
        """Shutdown the executor and wait for all futures to complete.

        Parameters
        ----------
        exc_type : type[BaseException] | None
            The exception type.

        exc_val : BaseException | None
            The exception instance.

        exc_tb : TracebackType | None
            The traceback object.

        Returns
        -------
        Literal[False]
            This method always returns :obj:`False`.
        """
        self.shutdown(wait=True)
        return False
