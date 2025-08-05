from aioplus import apairwise, arange


class TestApairwise:
    """Tests for `aioplus.apairwise`."""

    async def test__apairwise(self) -> None:
        """Case: default usage."""
        pairs = [pair async for pair in apairwise(arange(5))]

        assert pairs == [(0, 1), (1, 2), (2, 3), (3, 4)]

    async def test__apairwise__empty(self) -> None:
        """Case: empty iterable."""
        pairs = [pair async for pair in apairwise(arange(0))]

        assert not pairs

    async def test__apairwise__single_element(self) -> None:
        """Case: single element iterable."""
        pairs = [pair async for pair in apairwise(arange(1))]

        assert not pairs
