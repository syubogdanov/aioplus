import pytest

from aioplus import arange, asum


class TestParameters:
    """Parameter tests."""

    async def test__aiterable(self) -> None:
        """Case: non-iterable."""
        with pytest.raises(TypeError):
            await asum(None)


class TestFunction:
    """Function tests."""

    async def test__asum(self) -> None:
        """Case: default usage."""
        aiterable = arange(23)

        total = await asum(aiterable)

        assert total == 253

    async def test__asum__empty(self) -> None:
        """Case: `len(...) == 0`."""
        aiterable = arange(0)

        total = await asum(aiterable)

        assert total == 0

    async def test__asum__start(self) -> None:
        """Case: `start` provided."""
        aiterable = arange(23)

        total = await asum(aiterable, start=4)

        assert total == 257

    async def test__asum__start_and_empty(self) -> None:
        """Case: `len(...) == 0` & `start=...`."""
        aiterable = arange(0)

        total = await asum(aiterable, start=4)

        assert total == 4
