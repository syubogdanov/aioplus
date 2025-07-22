from aioplus import acount


class TestAcount:
    """Tests for `aioplus.acount`."""

    async def test__acount(self) -> None:
        """Case: default usage."""
        iterable = acount()
        iterator = aiter(iterable)

        nums: list[int] = []

        while len(nums) < 5:
            num = await anext(iterator)
            nums.append(num)

        assert nums == [0, 1, 2, 3, 4]

    async def test__acount__start(self) -> None:
        """Case: usage with start value."""
        iterable = acount(4)
        iterator = aiter(iterable)

        nums: list[int] = []

        while len(nums) < 5:
            num = await anext(iterator)
            nums.append(num)

        assert nums == [4, 5, 6, 7, 8]

    async def test__acount__step(self) -> None:
        """Case: usage with step value."""
        iterable = acount(0, 2)
        iterator = aiter(iterable)

        nums: list[int] = []

        while len(nums) < 5:
            num = await anext(iterator)
            nums.append(num)

        assert nums == [0, 2, 4, 6, 8]
