from aioplus import arange

import pytest


class TestArange:
    """Tests for `aioplus.arange`."""

    async def test__arange__one_parameter(self) -> None:
        """Case: one parameter."""
        nums = [num async for num in arange(10)]

        assert nums == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    async def test__arange__two_parameters(self) -> None:
        """Case: two parameters."""
        nums = [num async for num in arange(4, 10)]

        assert nums == [4, 5, 6, 7, 8, 9]

    async def test__arange__three_parameters(self) -> None:
        """Case: three parameters."""
        nums = [num async for num in arange(4, 23, 3)]

        assert nums == [4, 7, 10, 13, 16, 19, 22]

    async def test__arange__negative_step(self) -> None:
        """Case: negative step."""
        nums = [num async for num in arange(23, 4, -3)]

        assert nums == [23, 20, 17, 14, 11, 8, 5]

    async def test__arange__empty(self) -> None:
        """Case: empty range."""
        nums = [num async for num in arange(23, 4)]

        assert not nums

    async def test__arange__zero_step(self) -> None:
        """Case: zero step."""
        with pytest.raises(ValueError):
            [num async for num in arange(4, 23, 0)]
