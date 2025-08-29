import re

import pytest

from aioplus import amin, arange


class TestParameters:
    """Parameter tests."""

    async def test__aiterable(self) -> None:
        """Case: non-iterable."""
        with pytest.raises(TypeError):
            await amin(None)

    async def test__key(self) -> None:
        """Case: non-callable."""
        with pytest.raises(TypeError):
            await amin(arange(23), key="4")


class TestFunction:
    """Function tests."""

    async def test__amin(self) -> None:
        """Case: default usage."""
        aiterable = arange(23)

        smallest = await amin(aiterable)

        assert smallest == 0

    async def test__amin__empty(self) -> None:
        """Case: `len(...) == 0`."""
        aiterable = arange(0)

        with pytest.raises(ValueError, match=re.escape("amin(): empty iterable")):
            await amin(aiterable)

    async def test__amin__default(self) -> None:
        """Case: `default` provided."""
        aiterable = arange(0)

        smallest = await amin(aiterable, default=23)

        assert smallest == 23

    async def test__amin__single_element(self) -> None:
        """Case: `len(...) == 1`."""
        aiterable = arange(1)

        smallest = await amin(aiterable)

        assert smallest == 0

    async def test__amin__key(self) -> None:
        """Case: `key` provided."""
        aiterable = arange(5)

        smallest = await amin(aiterable, key=lambda x: -x)

        assert smallest == 4
