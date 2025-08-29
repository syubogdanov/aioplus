from pathlib import Path
from tempfile import gettempdir
from uuid import uuid4

import pytest


@pytest.fixture
def directory() -> Path:
    """Path to the temporary directory."""
    path = Path(gettempdir()) / "aioplus" / str(uuid4())
    path.mkdir(parents=True, exist_ok=True)
    return path


@pytest.fixture
def file(directory: Path) -> Path:
    """Path to the temporary file."""
    path = directory / str(uuid4())
    path.touch()
    return path
