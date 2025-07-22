from aioplus import aany, acount, arange


class TestAany:
    """Tests for `aioplus.aany`."""

    async def test__aany__true(self) -> None:
        """Case: return `True`."""
        iterator = (num == 0 async for num in arange(0, 2304, 2))

        flg = await aany(iterator)

        assert flg

    async def test__aany__false(self) -> None:
        """Case: return `False`."""
        iterator = (num < 0 async for num in arange(0, 2304, 2))

        flg = await aany(iterator)

        assert not flg

    async def test__aany__empty(self) -> None:
        """Case: return `False` if empty."""
        iterator = arange(0)

        flg = await aany(iterator)

        assert not flg

    async def test__aany__infinite(self) -> None:
        """Case: early return for infinite iterators."""
        iterator = (num > 0 async for num in acount())

        flg = await aany(iterator)

        assert flg
