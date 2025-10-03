import pytest

from aioplus import ahead, atabulate, awaitify


class TestParameters:
    """Parameter tests."""

    def test__func(self) -> None:
        """Case: non-callable."""
        with pytest.raises(TypeError):
            atabulate(None)

    def test__func__not_coroutine(self) -> None:
        """Case: non-coroutine function."""
        with pytest.raises(TypeError):
            atabulate(abs)

    def test__start(self) -> None:
        """Case: non-integer."""
        afunc = awaitify(abs)
        with pytest.raises(TypeError):
            atabulate(afunc, start="4")


class TestFunction:
    """Function tests."""

    async def test__atabulate(self) -> None:
        """Case: default usage."""
        afunc = awaitify(lambda x: x * x)

        aiterable = atabulate(afunc)
        squares = [num async for num in ahead(aiterable, n=5)]

        assert squares == [0, 1, 4, 9, 16]

    async def test__atabulate__start(self) -> None:
        """Case: `start != 0`."""
        afunc = awaitify(lambda x: x * x)

        aiterable = atabulate(afunc, start=3)
        squares = [num async for num in ahead(aiterable, n=5)]

        assert squares == [9, 16, 25, 36, 49]
