import re

import pytest

from aioplus import afirst, arange


class TestParameters:
    """Parameter tests."""

    async def test__aiterable(self) -> None:
        """Case: non-iterable."""
        with pytest.raises(TypeError):
            await afirst(None)


class TestFunction:
    """Function tests."""

    async def test__afirst(self) -> None:
        """Case: default usage."""
        aiterable = arange(4, 23)

        value = await afirst(aiterable)

        assert value == 4

    async def test__afirst__empty(self) -> None:
        """Case: `len(...) == 0`."""
        aiterable = arange(0)

        with pytest.raises(IndexError, match=re.escape("afirst(): empty iterable")):
            await afirst(aiterable)

    async def test__afirst__default(self) -> None:
        """Case: `default` provided."""
        aiterable = arange(0)

        value = await afirst(aiterable, default=23)

        assert value == 23
