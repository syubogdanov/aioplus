from aioplus import aenumerate, arange


class TestAenumerate:
    """Tests for `aioplus.aenumerate`."""

    async def test__aenumerate(self) -> None:
        """Case: default usage."""
        pairs = [pair async for pair in aenumerate(arange(5))]

        assert pairs == [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]

    async def test__aenumerate__start(self) -> None:
        """Case: with start parameter."""
        pairs = [pair async for pair in aenumerate(arange(4), start=10)]

        assert pairs == [(10, 0), (11, 1), (12, 2), (13, 3)]

    async def test__aenumerate__negative_start(self) -> None:
        """Case: with negative start parameter."""
        pairs = [pair async for pair in aenumerate(arange(6), start=-2)]

        assert pairs == [(-2, 0), (-1, 1), (0, 2), (1, 3), (2, 4), (3, 5)]
