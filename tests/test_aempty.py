import pytest

from aioplus import aempty, arange


class TestParameters:
    """Parameter tests."""

    async def test__aiterable(self) -> None:
        """Case: non-iterable."""
        with pytest.raises(TypeError):
            await aempty(None)


class TestFunction:
    """Function tests."""

    async def test__aempty(self) -> None:
        """Case: default usage."""
        aiterable = arange(23)

        empty_flg = await aempty(aiterable)

        assert not empty_flg

    async def test__alen__empty(self) -> None:
        """Case: `len(...) == 0."""
        aiterable = arange(0)

        empty_flg = await aempty(aiterable)

        assert empty_flg
