import pytest

from aioplus import CallerThreadExecutor


class TestParameters:
    """Parameter tests."""

    async def test__max_workers(self) -> None:
        """Case: non-integer."""
        with pytest.raises(TypeError):
            CallerThreadExecutor(max_workers="23")

    async def test__max_workers__negative(self) -> None:
        """Case: `max_workers < 0`."""
        with pytest.raises(ValueError, match="'max_workers' must be positive"):
            CallerThreadExecutor(max_workers=-23)

    async def test__max_workers__zero(self) -> None:
        """Case: `max_workers == 0`."""
        with pytest.raises(ValueError, match="'max_workers' must be positive"):
            CallerThreadExecutor(max_workers=0)

    async def test__thread_name_prefix(self) -> None:
        """Case: non-string."""
        with pytest.raises(TypeError):
            CallerThreadExecutor(thread_name_prefix=23)

    async def test__initializer(self) -> None:
        """Case: non-callable."""
        with pytest.raises(TypeError):
            CallerThreadExecutor(initializer=23)

    async def test__initargs(self) -> None:
        """Case: non-tuple."""
        with pytest.raises(TypeError):
            CallerThreadExecutor(initargs=23)


class TestClass:
    """Class tests."""

    async def test__caller_thread_executor__submit(self) -> None:
        """Case: submit a callable."""
        executor = CallerThreadExecutor()

        future = executor.submit(lambda x: x + 4, 23)
        result = future.result()

        assert result == 27

    async def test__caller_thread_executor__map(self) -> None:
        """Case: map a function over an iterable."""
        executor = CallerThreadExecutor()

        iterator = executor.map(lambda x: x + 23, range(4))
        results = list(iterator)

        assert results == [23, 24, 25, 26]

    async def test__caller_thread_executor__submit_after_shutdown(self) -> None:
        """Case: submit a callable after shutdown."""
        executor = CallerThreadExecutor()

        executor.shutdown()
        with pytest.raises(RuntimeError):
            executor.submit(lambda x: x + 4, 23)

    async def test__caller_thread_executor__map_after_shutdown(self) -> None:
        """Case: submit a callable after shutdown."""
        executor = CallerThreadExecutor()

        executor.shutdown()
        with pytest.raises(RuntimeError):
            list(executor.map(lambda x: x + 23, range(4)))

    async def test__caller_thread_executor__midtime_shutdown(self) -> None:
        """Case: submit a callable during shutdown."""
        executor = CallerThreadExecutor()

        iterator = executor.map(lambda x: x + 23, range(4))
        next(iterator)

        executor.shutdown()

        with pytest.raises(RuntimeError):
            next(iterator)
