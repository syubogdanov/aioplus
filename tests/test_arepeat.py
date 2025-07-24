import pytest

from aioplus import arepeat


class TestArepeat:
    """Tests for `aioplus.arepeat`."""

    async def test__arepeat(self) -> None:
        """Case: default usage."""
        nums = [num async for num in arepeat(23, times=4)]

        assert nums == [23, 23, 23, 23]

    async def test__arepeat__zero_times(self) -> None:
        """Case: zero times."""
        nums = [num async for num in arepeat(23, times=0)]

        assert not nums

    async def test__arepeat__negative_times(self) -> None:
        """Case: negative times."""
        with pytest.raises(ValueError, match="'times' must be non-negative"):
            [num async for num in arepeat(23, times=-3)]

    async def test__arepeat__infinite(self) -> None:
        """Case: infinite repetition."""
        aiterable = arepeat(0)
        aiterator = aiter(aiterable)

        nums: list[int] = []

        while len(nums) < 10:
            num = await anext(aiterator)
            nums.append(num)

        assert nums == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
