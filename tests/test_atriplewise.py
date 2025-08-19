from aioplus import arange, atriplewise


class TestAtriplewise:
    """Tests for `aioplus.atriplewise`."""

    async def test__atriplewise(self) -> None:
        """Case: default usage."""
        triplets = [triplet async for triplet in atriplewise(arange(5))]

        assert triplets == [(0, 1, 2), (1, 2, 3), (2, 3, 4)]

    async def test__atriplewise__empty(self) -> None:
        """Case: empty iterable."""
        triplets = [triplet async for triplet in atriplewise(arange(0))]

        assert not triplets

    async def test__atriplewise__single_element(self) -> None:
        """Case: single element iterable."""
        triplets = [triplet async for triplet in atriplewise(arange(1))]

        assert not triplets

    async def test__atriplewise__two_elements(self) -> None:
        """Case: two elements in the iterable."""
        triplets = [triplet async for triplet in atriplewise(arange(2))]

        assert not triplets
