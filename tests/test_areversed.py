from aioplus import arange, areversed


class TestAreversed:
    """Tests for `aioplus.areversed`."""

    async def test__areversed(self) -> None:
        """Test the areversed function."""
        nums = [num async for num in areversed(arange(5))]

        assert nums == [4, 3, 2, 1, 0]

    async def test__areversed__empty(self) -> None:
        """Test areversed with an empty range."""
        nums = [num async for num in areversed(arange(0))]

        assert not nums
