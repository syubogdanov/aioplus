import re

import pytest

from aioplus import aminmax, arange


class TestParameters:
    """Parameter tests."""

    async def test__aiterable(self) -> None:
        """Case: non-iterable."""
        with pytest.raises(TypeError):
            await aminmax(None)

    async def test__key(self) -> None:
        """Case: non-callable."""
        with pytest.raises(TypeError):
            await aminmax(arange(23), key="4")

    async def test__default(self) -> None:
        """Case: non-tuple."""
        with pytest.raises(TypeError):
            await aminmax(arange(23), default=4)


class TestFunction:
    """Function tests."""

    async def test__aminmax(self) -> None:
        """Case: default usage."""
        aiterable = arange(23)

        smallest, largest = await aminmax(aiterable)

        assert (smallest, largest) == (0, 22)

    async def test__aminmax__empty(self) -> None:
        """Case: `len(...) == 0`."""
        aiterable = arange(0)

        with pytest.raises(ValueError, match=re.escape("aminmax(): empty iterable")):
            await aminmax(aiterable)

    async def test__aminmax__default(self) -> None:
        """Case: `default` provided."""
        aiterable = arange(0)

        smallest, largest = await aminmax(aiterable, default=(23, 4))

        assert (smallest, largest) == (23, 4)

    async def test__aminmax__single_element(self) -> None:
        """Case: `len(...) == 1`."""
        aiterable = arange(1)

        smallest, largest = await aminmax(aiterable)

        assert (smallest, largest) == (0, 0)

    async def test__aminmax__key(self) -> None:
        """Case: `key` provided."""
        aiterable = arange(5)

        smallest, largest = await aminmax(aiterable, key=lambda x: -x)

        assert (smallest, largest) == (4, 0)
