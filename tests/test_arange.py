from aioplus import arange

import pytest


class TestArange:
    """Tests for `aioplus.arange`."""

    async def test__arange__one_parameter(self) -> None:
        """Case: one parameter."""
        stop = 23

        async_nums = [num async for num in arange(stop)]
        sync_nums = list(range(stop))

        assert async_nums == sync_nums

    async def test__arange__two_parameters(self) -> None:
        """Case: two parameters."""
        start = 4
        stop = 23

        async_nums = [num async for num in arange(start, stop)]
        sync_nums = list(range(start, stop))

        assert async_nums == sync_nums

    async def test__arange__three_parameters(self) -> None:
        """Case: three parameters."""
        start = 4
        stop = 23
        step = 3

        async_nums = [num async for num in arange(start, stop, step)]
        sync_nums = list(range(start, stop, step))

        assert async_nums == sync_nums

    async def test__arange__negative_step(self) -> None:
        """Case: negative step."""
        start = 23
        stop = 4
        step = -3

        async_nums = [num async for num in arange(start, stop, step)]
        sync_nums = list(range(start, stop, step))

        assert async_nums == sync_nums

    async def test__arange__empty(self) -> None:
        """Case: empty range."""
        start = 4
        stop = start

        async_nums = [num async for num in arange(start, stop)]
        sync_nums = list(range(start, stop))

        assert async_nums == sync_nums

    async def test__arange__zero_step(self) -> None:
        """Case: zero step."""
        with pytest.raises(ValueError):
            [num async for num in arange(4, 23, 0)]
