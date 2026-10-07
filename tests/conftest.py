import shutil
from pathlib import Path

import pytest

SAMPLE_DATA = Path(__file__).resolve().parent.parent / "sample_data"


@pytest.fixture
def workdir(tmp_path, monkeypatch):
    """A scratch copy of sample_data, used as the current directory."""
    for item in SAMPLE_DATA.iterdir():
        if item.is_file():
            shutil.copy(item, tmp_path / item.name)
    monkeypatch.chdir(tmp_path)
    return tmp_path
