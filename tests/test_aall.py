from aioplus import aall, acount, arange


class TestAall:
    """Tests for `aioplus.aall`."""

    async def test__aall__true(self) -> None:
        """Case: return `True`."""
        aiterator = (num >= 0 async for num in arange(0, 2304, 2))

        flg = await aall(aiterator)

        assert flg

    async def test__aall__false(self) -> None:
        """Case: return `False`."""
        aiterator = (num <= 0 async for num in arange(0, 2304, 2))

        flg = await aall(aiterator)

        assert not flg

    async def test__aall__empty(self) -> None:
        """Case: return `True` if empty."""
        aiterator = arange(0)

        flg = await aall(aiterator)

        assert flg

    async def test__aall__infinite(self) -> None:
        """Case: early return for infinite iterators."""
        aiterator = (num < 0 async for num in acount())

        flg = await aall(aiterator)

        assert not flg
