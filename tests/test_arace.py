import re

from collections.abc import AsyncGenerator
from contextlib import aclosing

import pytest

from aioplus import arace, arange


class TestParameters:
    """Parameter tests."""

    def test__aiterables(self) -> None:
        """Case: non-iterable."""
        with pytest.raises(TypeError):
            arace(None)

    def test__aiterables__strict(self) -> None:
        """Case: non-iterable."""
        with pytest.raises(TypeError):
            arace(None, strict=23)

    async def test__arace__empty(self) -> None:
        """Case: empty call."""
        with pytest.raises(ValueError, match=re.escape("'*aiterables' must be non-empty")):
            arace()


class TestFunction:
    """Function tests."""

    async def test__arace(self) -> None:
        """Case: default usage."""
        aiterables = [arange(0, 3), arange(3, 6), arange(6, 9)]

        nums = [num async for num in arace(*aiterables)]

        assert sorted(nums) == [0, 1, 2, 3, 4, 5, 6, 7, 8]

    async def test__arace__one_exception(self) -> None:
        """Case: one exception."""

        async def gen1() -> AsyncGenerator[int]:
            if True:
                raise RuntimeError
            yield 1

        async def gen2() -> AsyncGenerator[int]:
            yield 2

        async with aclosing(gen1()) as nums1, aclosing(gen2()) as nums2:
            with pytest.raises(ExceptionGroup) as group:
                [num async for num in arace(nums1, nums2)]

        assert len(group.value.exceptions) == 1

    async def test__arace__two_exceptions(self) -> None:
        """Case: two exceptions."""

        async def gen1() -> AsyncGenerator[int]:
            if True:
                raise RuntimeError(1)
            yield 1

        async def gen2() -> AsyncGenerator[int]:
            if True:
                raise RuntimeError(2)
            yield 2

        async with aclosing(gen1()) as nums1, aclosing(gen2()) as nums2:
            with pytest.raises(ExceptionGroup) as group:
                [num async for num in arace(nums1, nums2)]

        assert len(group.value.exceptions) == 2
