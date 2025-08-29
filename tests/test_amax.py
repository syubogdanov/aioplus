import re

import pytest

from aioplus import amax, arange


class TestParameters:
    """Parameter tests."""

    async def test__aiterable(self) -> None:
        """Case: non-iterable."""
        with pytest.raises(TypeError):
            await amax(None)

    async def test__key(self) -> None:
        """Case: non-callable."""
        with pytest.raises(TypeError):
            await amax(arange(23), key="4")


class TestFunction:
    """Function tests."""

    async def test__amax(self) -> None:
        """Case: default usage."""
        aiterable = arange(23)

        largest = await amax(aiterable)

        assert largest == 22

    async def test__amax__empty(self) -> None:
        """Case: `len(...) == 0`."""
        aiterable = arange(0)

        with pytest.raises(ValueError, match=re.escape("amax(): empty iterable")):
            await amax(aiterable)

    async def test__amax__default(self) -> None:
        """Case: `default` provided."""
        aiterable = arange(0)

        largest = await amax(aiterable, default=23)

        assert largest == 23

    async def test__amax__single_element(self) -> None:
        """Case: `len(...) == 1`."""
        aiterable = arange(1)

        largest = await amax(aiterable)

        assert largest == 0

    async def test__amax__key(self) -> None:
        """Case: `key` provided."""
        aiterable = arange(5)

        largest = await amax(aiterable, key=lambda x: -x)

        assert largest == 0
