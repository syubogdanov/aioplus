import pytest

from aioplus import aenumerate, arange


class TestParameters:
    """Parameter tests."""

    def test__aiterable(self) -> None:
        """Case: non-iterable."""
        with pytest.raises(TypeError):
            aenumerate(None)

    def test__start(self) -> None:
        """Case: non-integer."""
        with pytest.raises(TypeError):
            aenumerate(arange(23), start="4")


class TestFunction:
    """Function tests."""

    async def test__aenumerate(self) -> None:
        """Case: default usage."""
        aiterable = arange(5)

        pairs = [pair async for pair in aenumerate(aiterable)]

        assert pairs == [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]

    async def test__aenumerate__start(self) -> None:
        """Case: `start` provided."""
        aiterable = arange(4)

        pairs = [pair async for pair in aenumerate(aiterable, start=10)]

        assert pairs == [(10, 0), (11, 1), (12, 2), (13, 3)]

    async def test__aenumerate__negative_start(self) -> None:
        """Case: negative `start`."""
        aiterable = arange(6)

        pairs = [pair async for pair in aenumerate(aiterable, start=-2)]

        assert pairs == [(-2, 0), (-1, 1), (0, 2), (1, 3), (2, 4), (3, 5)]
