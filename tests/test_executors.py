from aioplus import CurrentThreadExecutor, anextify


class TestCurrentThreadExecutor:
    """Tests for `aioplus.CurrentThreadExecutor`."""

    async def test__current_thread_executor(self) -> None:
        """Case: default behavior."""
        executor = CurrentThreadExecutor()

        iterable = [1, 2, 3, 4, 5, 6, 7, 8]
        aiterable = anextify(iterable, executor=executor)

        nums = [num async for num in aiterable]

        assert nums == [1, 2, 3, 4, 5, 6, 7, 8]
