from aioplus import CallerThreadExecutor, anextify


class TestCallerThreadExecutor:
    """Tests for `aioplus.CallerThreadExecutor`."""

    async def test__caller_thread_executor(self) -> None:
        """Case: default behavior."""
        executor = CallerThreadExecutor()

        iterable = [1, 2, 3, 4, 5, 6, 7, 8]
        aiterable = anextify(iterable, executor=executor)

        nums = [num async for num in aiterable]

        assert nums == [1, 2, 3, 4, 5, 6, 7, 8]
