import pytest

from aioplus import aall, acount, arange


class TestParameters:
    """Parameter tests."""

    async def test__aiterable(self) -> None:
        """Case: non-iterable."""
        with pytest.raises(TypeError):
            await aall(None)


class TestFunction:
    """Function tests."""

    async def test__aall__true(self) -> None:
        """Case: return `True`."""
        aiterable = (num > 0 async for num in arange(4, 23))

        flg = await aall(aiterable)

        assert flg

    async def test__aall__false(self) -> None:
        """Case: return `False`."""
        aiterable = (num < 0 async for num in arange(4, 23))

        flg = await aall(aiterable)

        assert not flg

    async def test__aall__empty(self) -> None:
        """Case: empty iterable."""
        aiterable = arange(0)

        flg = await aall(aiterable)

        assert flg

    async def test__aall__short_circuit(self) -> None:
        """Case: short-circuit evaluation."""
        aiterable = (num < 0 async for num in acount())

        flg = await aall(aiterable)

        assert not flg
