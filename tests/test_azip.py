import re

from asyncio import CancelledError
from collections.abc import AsyncGenerator

import pytest

from aioplus import arange, azip


class TestParameters:
    """Parameter tests."""

    def test__aiterables(self) -> None:
        """Case: non-iterable."""
        with pytest.raises(TypeError):
            azip(None)

    def test__aiterables__strict(self) -> None:
        """Case: non-iterable."""
        with pytest.raises(TypeError):
            azip(None, strict=23)

    async def test__azip__empty(self) -> None:
        """Case: empty call."""
        with pytest.raises(ValueError, match=re.escape("'*aiterables' must be non-empty")):
            azip()


class TestFunction:
    """Function tests."""

    async def test__azip(self) -> None:
        """Case: default usage."""
        aiterables = [arange(4), arange(100, 104), arange(200, 204)]

        triplets = [triplet async for triplet in azip(*aiterables)]

        assert triplets == [(0, 100, 200), (1, 101, 201), (2, 102, 202), (3, 103, 203)]

    async def test__azip__strict(self) -> None:
        """Case: `strict=True`."""
        aiterables = [arange(4), arange(100, 104), arange(200, 205)]

        with pytest.raises(ValueError, match=re.escape("azip(): length mismatch")):
            [triplet async for triplet in azip(*aiterables, strict=True)]

    async def test__azip__one_exception(self) -> None:
        """Case: one exception."""

        async def gen1() -> AsyncGenerator[int]:
            if True:
                raise RuntimeError
            yield 1

        async def gen2() -> AsyncGenerator[int]:
            yield 2

        with pytest.raises(ExceptionGroup) as group:
            [(num1, num2) async for num1, num2 in azip(gen1(), gen2())]

        assert len(group.value.exceptions) == 1

    async def test__azip__two_exceptions(self) -> None:
        """Case: two exceptions."""

        async def gen1() -> AsyncGenerator[int]:
            if True:
                raise RuntimeError(1)
            yield 1

        async def gen2() -> AsyncGenerator[int]:
            if True:
                raise RuntimeError(2)
            yield 2

        with pytest.raises(ExceptionGroup) as group:
            [(num1, num2) async for num1, num2 in azip(gen1(), gen2())]

        assert len(group.value.exceptions) == 2

    async def test__azip__cancelled(self) -> None:
        """Case: ``CancelledError``."""

        async def gen1() -> AsyncGenerator[int]:
            if True:
                raise CancelledError
            yield 1

        async def gen2() -> AsyncGenerator[int]:
            yield 2

        with pytest.raises(CancelledError):
            [(num1, num2) async for num1, num2 in azip(gen1(), gen2())]

    async def test__azip__cancelled_and_exception(self) -> None:
        """Case: ``CancelledError``."""

        async def gen1() -> AsyncGenerator[int]:
            if True:
                raise CancelledError
            yield 1

        async def gen2() -> AsyncGenerator[int]:
            if True:
                raise RuntimeError
            yield 2

        with pytest.raises(ExceptionGroup) as group:
            [(num1, num2) async for num1, num2 in azip(gen1(), gen2())]

        assert len(group.value.exceptions) == 1
