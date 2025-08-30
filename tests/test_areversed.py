import pytest

from aioplus import arange, areversed


class TestParameters:
    """Parameter tests."""

    def test__aiterable(self) -> None:
        """Case: non-iterable."""
        with pytest.raises(TypeError):
            areversed(None)


class TestFunction:
    """Function tests."""

    async def test__areversed(self) -> None:
        """Case: default usage."""
        aiterable = arange(5)

        nums = [num async for num in areversed(aiterable)]

        assert nums == [4, 3, 2, 1, 0]

    async def test__areversed__empty(self) -> None:
        """Case: `len(...) == 0`."""
        aiterable = arange(0)

        nums = [num async for num in areversed(aiterable)]

        assert not nums
