from aioplus import acount


class TestAcount:
    """Tests for `aioplus.acount`."""

    async def test__acount(self) -> None:
        """Case: default usage."""
        aiterable = acount()
        aiterator = aiter(aiterable)

        nums: list[int] = []

        while len(nums) < 5:
            num = await anext(aiterator)
            nums.append(num)

        assert nums == [0, 1, 2, 3, 4]

    async def test__acount__start(self) -> None:
        """Case: usage with start value."""
        aiterable = acount(4)
        aiterator = aiter(aiterable)

        nums: list[int] = []

        while len(nums) < 5:
            num = await anext(aiterator)
            nums.append(num)

        assert nums == [4, 5, 6, 7, 8]

    async def test__acount__step(self) -> None:
        """Case: usage with step value."""
        aiterable = acount(0, 2)
        aiterator = aiter(aiterable)

        nums: list[int] = []

        while len(nums) < 5:
            num = await anext(aiterator)
            nums.append(num)

        assert nums == [0, 2, 4, 6, 8]

    async def test__acount__zero_step(self) -> None:
        """Case: usage with zero step value."""
        aiterable = acount(0, 0)
        aiterator = aiter(aiterable)

        nums: list[int] = []

        while len(nums) < 5:
            num = await anext(aiterator)
            nums.append(num)

        assert nums == [0, 0, 0, 0, 0]
