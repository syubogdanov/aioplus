import pytest

from aioplus import CallerThreadExecutor, anextify


class TestCallerThreadExecutor:
    """Tests for `aioplus.CallerThreadExecutor`."""

    async def test__caller_thread_executor__submit(self) -> None:
        """Case: submit a callable."""
        executor = CallerThreadExecutor()

        future = executor.submit(lambda x: x + 1, 1)
        result = future.result()

        assert result == 2

    async def test__caller_thread_executor__map(self) -> None:
        """Case: map a function over an iterable."""
        executor = CallerThreadExecutor()

        results = list(executor.map(lambda x: x + 1, range(5)))

        assert results == [1, 2, 3, 4, 5]

    async def test__caller_thread_executor__submit_after_shutdown(self) -> None:
        """Case: submit a callable after shutdown."""
        executor = CallerThreadExecutor()
        executor.shutdown()

        with pytest.raises(RuntimeError):
            executor.submit(lambda x: x + 1, 1)

    async def test__caller_thread_executor__map_after_shutdown(self) -> None:
        """Case: submit a callable after shutdown."""
        executor = CallerThreadExecutor()
        executor.shutdown()

        with pytest.raises(RuntimeError):
            list(executor.map(lambda x: x + 1, range(5)))

    async def test__caller_thread_executor__midtime_shutdown(self) -> None:
        """Case: submit a callable during shutdown."""
        executor = CallerThreadExecutor()

        iterator = executor.map(lambda x: x + 1, range(5))
        executor.shutdown()

        with pytest.raises(RuntimeError):
            next(iterator)

    async def test__caller_thread_executor__anextify(self) -> None:
        """Case: default behavior."""
        executor = CallerThreadExecutor()

        iterable = [1, 2, 3, 4, 5, 6, 7, 8]
        aiterable = anextify(iterable, executor=executor)

        nums = [num async for num in aiterable]

        assert nums == [1, 2, 3, 4, 5, 6, 7, 8]
