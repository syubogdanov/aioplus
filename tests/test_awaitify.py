import json
import tomllib

from pathlib import Path
from tomllib import TOMLDecodeError

import pytest

from aioplus import CallerThreadExecutor, awaitify


JSON = {"aioplus": "awaitify"}


class TestParameters:
    """Parameter tests."""

    def test__func(self) -> None:
        """Case: non-callable."""
        with pytest.raises(TypeError):
            awaitify(None)

    def test__executor(self) -> None:
        """Case: non-executor."""
        with pytest.raises(TypeError):
            awaitify(print, executor=23)


class TestFunction:
    """Function tests."""

    async def test__awaitify(self, file: Path) -> None:
        """Case: default usage."""
        file.touch(exist_ok=True)

        aexists = awaitify(file.exists)
        exists_flg = await aexists()

        assert exists_flg

    async def test__awaitify__args(self, file: Path) -> None:
        """Case: `*args`."""
        with file.open(mode="w") as fd:
            json.dump(JSON, fd)

        aload = awaitify(json.load)
        with file.open() as fd:
            obj = await aload(fd)

        assert obj == JSON

    async def test__awaitify__kwargs(self, file: Path) -> None:
        """Case: `**kwargs`."""
        with file.open(mode="w") as fd:
            json.dump(JSON, fd)

        aload = awaitify(json.load)
        with file.open() as fd:
            obj = await aload(fp=fd)

        assert obj == JSON

    async def test__awaitify__exception(self, file: Path) -> None:
        """Case: exception raised."""
        with file.open(mode="w") as fd:
            json.dump(JSON, fd)

        aload = awaitify(tomllib.load)
        with file.open(mode="rb") as fd, pytest.raises(TOMLDecodeError):
            await aload(fd)

    async def test__awaitify__executor(self, file: Path) -> None:
        """Case: `executor` provided."""
        file.touch(exist_ok=True)

        aexists = awaitify(file.exists, executor=CallerThreadExecutor())
        exists_flg = await aexists()

        assert exists_flg
