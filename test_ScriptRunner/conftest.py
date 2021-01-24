"""Fixtures for `test_ScriptRunner`."""

import sys

import pytest

sys.path.append("ScriptRunner/")


@pytest.fixture
def test_dir(tmpdir):
    """
    Returns path to the `test_dir`.
    """
    return tmpdir.mkdir("test_dir")


@pytest.fixture
def test_file(test_dir):
    """
    Returns path to the file with `filename`  and `content` at `test_dir`.
    """

    def wrapper(filename: str, content: str):
        file = test_dir / filename
        file.write_text(content, encoding="utf-8")
        return file

    return wrapper
