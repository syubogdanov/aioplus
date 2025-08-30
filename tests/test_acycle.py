import pytest

from aioplus import acycle, ahead, arange


class TestParameters:
    """Parameter tests."""

    def test__aiterable(self) -> None:
        """Case: non-iterable."""
        with pytest.raises(TypeError):
            acycle(None)


class TestFunction:
    """Function tests."""

    async def test__acycle(self) -> None:
        """Case: default usage."""
        aiterable = arange(4)

        nums = [num async for num in ahead(acycle(aiterable), n=10)]

        assert nums == [0, 1, 2, 3, 0, 1, 2, 3, 0, 1]

    async def test__acycle_empty(self) -> None:
        """Case: `len(...) == 0`."""
        aiterable = arange(0)

        nums = [num async for num in acycle(aiterable)]

        assert not nums
