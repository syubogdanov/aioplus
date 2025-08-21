from pathlib import Path
from tempfile import gettempdir
from uuid import uuid4

import pytest


@pytest.fixture
def tempdir() -> Path:
    """Path to the temporary directory."""
    path = Path(gettempdir()) / "aioplus" / str(uuid4())
    path.mkdir(parents=True, exist_ok=True)
    return path


@pytest.fixture
def tempfile(tempdir: Path) -> Path:
    """Path to the temporary file."""
    path = tempdir / str(uuid4())
    path.touch()
    return path
