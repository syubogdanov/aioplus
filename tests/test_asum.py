from aioplus import arange, asum


class TestAsum:
    """Tests for `aioplus.asum`."""

    async def test__asum(self) -> None:
        """Case: default behavior."""
        aiterator = arange(23)

        total = await asum(aiterator)

        assert total == 253

    async def test__asum__empty(self) -> None:
        """Case: empty iterable."""
        aiterator = arange(0)

        total = await asum(aiterator)

        assert total == 0

    async def test__asum__start(self) -> None:
        """Case: start provided."""
        aiterator = arange(23)

        total = await asum(aiterator, start=4)

        assert total == 257

    async def test__asum__start_and_empty(self) -> None:
        """Case: start provided and iterable is empty."""
        aiterator = arange(0)

        total = await asum(aiterator, start=4)

        assert total == 4
