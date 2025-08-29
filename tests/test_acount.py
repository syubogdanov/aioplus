import pytest

from aioplus import acount, ahead


class TestParameters:
    """Parameter tests."""

    async def test__start(self) -> None:
        """Case: non-integer."""
        with pytest.raises(TypeError):
            acount("23")

    async def test__step(self) -> None:
        """Case: non-integer."""
        with pytest.raises(TypeError):
            acount(4, "23")


class TestFunction:
    """Function tests."""

    async def test__acount(self) -> None:
        """Case: default usage."""
        aiterable = acount()

        nums = [num async for num in ahead(aiterable, n=5)]

        assert nums == [0, 1, 2, 3, 4]

    async def test__acount__start(self) -> None:
        """Case: `start` provided."""
        aiterable = acount(start=4)

        nums = [num async for num in ahead(aiterable, n=5)]

        assert nums == [4, 5, 6, 7, 8]

    async def test__acount__step(self) -> None:
        """Case: `step` provided."""
        aiterable = acount(step=2)

        nums = [num async for num in ahead(aiterable, n=5)]

        assert nums == [0, 2, 4, 6, 8]

    async def test__acount__zero_step(self) -> None:
        """Case: `step == 0`."""
        aiterable = acount(step=0)

        nums = [num async for num in ahead(aiterable, n=5)]

        assert nums == [0, 0, 0, 0, 0]
