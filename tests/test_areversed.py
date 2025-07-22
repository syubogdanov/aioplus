from aioplus import arange, areversed


class TestAreversed:
    """Tests for `aioplus.areversed`."""

    async def test_areversed(self):
        """Test the areversed function."""
        start = 1
        stop = 10

        async_nums = [num async for num in areversed(arange(start, stop))]
        sync_nums = list(reversed(range(start, stop)))

        assert async_nums == sync_nums

    async def test_areversed_empty(self):
        """Test areversed with an empty range."""
        start = 0
        stop = start

        async_nums = [num async for num in areversed(arange(start, stop))]

        assert not async_nums
