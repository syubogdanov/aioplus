import pytest

from aioplus import arange, atriplewise


class TestParameters:
    """Parameter tests."""

    def test__aiterable(self) -> None:
        """Case: non-iterable."""
        with pytest.raises(TypeError):
            atriplewise(None)


class TestFunction:
    """Function tests."""

    async def test__atriplewise(self) -> None:
        """Case: default usage."""
        aiterable = arange(5)

        triplets = [triplet async for triplet in atriplewise(aiterable)]

        assert triplets == [(0, 1, 2), (1, 2, 3), (2, 3, 4)]

    async def test__atriplewise__empty(self) -> None:
        """Case: `len(...) == 0`."""
        aiterable = arange(0)

        triplets = [triplet async for triplet in atriplewise(aiterable)]

        assert not triplets

    async def test__atriplewise__single_element(self) -> None:
        """Case: `len(...) == 1`."""
        aiterable = arange(1)

        triplets = [triplet async for triplet in atriplewise(aiterable)]

        assert not triplets

    async def test__atriplewise__two_elements(self) -> None:
        """Case: `len(...) == 2`."""
        aiterable = arange(2)

        triplets = [triplet async for triplet in atriplewise(aiterable)]

        assert not triplets
