import pytest

from aioplus import apairwise, arange


class TestParameters:
    """Parameter tests."""

    async def test__aiterable(self) -> None:
        """Case: non-iterable."""
        with pytest.raises(TypeError):
            apairwise(None)


class TestFunction:
    """Function tests."""

    async def test__apairwise(self) -> None:
        """Case: default usage."""
        aiterable = arange(5)

        pairs = [pair async for pair in apairwise(aiterable)]

        assert pairs == [(0, 1), (1, 2), (2, 3), (3, 4)]

    async def test__apairwise__empty(self) -> None:
        """Case: `len(...) == 0`."""
        aiterable = arange(0)

        pairs = [pair async for pair in apairwise(aiterable)]

        assert not pairs

    async def test__apairwise__single_element(self) -> None:
        """Case: `len(...) == 1`."""
        aiterable = arange(1)

        pairs = [pair async for pair in apairwise(aiterable)]

        assert not pairs
