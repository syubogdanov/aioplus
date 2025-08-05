from aioplus import acycle, arange


class TestAcycle:
    """Tests for `aioplus.acycle`."""

    async def test__acycle(self) -> None:
        """Case: default usage."""
        aiterable = acycle(arange(4))
        aiterator = aiter(aiterable)

        nums: list[int] = []

        while len(nums) < 10:
            num = await anext(aiterator)
            nums.append(num)

        assert nums == [0, 1, 2, 3, 0, 1, 2, 3, 0, 1]

    async def test__acycle_empty(self) -> None:
        """Case: empty iterable."""
        nums = [num async for num in acycle(arange(0))]

        assert not nums
