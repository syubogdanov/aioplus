import pytest

from aioplus import alen, arange


class TestParameters:
    """Parameter tests."""

    async def test__aiterable(self) -> None:
        """Case: non-iterable."""
        with pytest.raises(TypeError):
            await alen(None)


class TestFunction:
    """Function tests."""

    async def test__alen(self) -> None:
        """Case: default behavior."""
        aiterator = arange(23)

        length = await alen(aiterator)

        assert length == 23

    async def test__alen__empty(self) -> None:
        """Case: `len(...) == 0."""
        aiterator = arange(0)

        length = await alen(aiterator)

        assert length == 0
