"""Unit tests for `Task` from `ScriptRunner.taskhandler`."""

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from ScriptRunner.taskhandler import Task

CONFIG_NAME = "config.json"
CONFIG_CONTENT = """{
    "priority": 1,
    "language_args": ["python"],
    "script": "name.py",
    "script_args": ["arg", "arg"],
    "failures": "stop",
    "next_config": false
}"""
CONFIG_TASK = Task(1, ["python"], "name.py", ["arg", "arg"], "stop", False)


@pytest.fixture
def mock_read_file_and_write_config(monkeypatch, test_file):
    """
    Mocks `config_handler.read_file` method for `CONFIG_CONTENT`
    returning and writes `CONFIG_NAME` with `CONFIG_CONTENT`.
    """
    monkeypatch.setattr(
        "ScriptRunner.taskhandler.config_handler.read_file",
        MagicMock(return_value=CONFIG_CONTENT),
    )
    test_file(CONFIG_NAME, CONFIG_CONTENT)


class TestNextTask:
    """Wraps tests for `Task.next_task`."""

    @staticmethod
    def test_without_next_config():
        """
        Passes test if `CONFIG_TASK.next_task` is `False`.
        """
        assert not CONFIG_TASK.next_task

    @staticmethod
    def test_with_next_config(mock_read_file_and_write_config):
        """
        Passes test if `CONFIG_TASK.next_task` returns is `CONFIG_TASK`.
        """
        task = Task(
            priority=2,
            language_args=["python"],
            script="name.py",
            script_args=["arg"],
            failures="stop",
            next_config=CONFIG_NAME,
        )
        assert task.next_task == CONFIG_TASK


def test_from_config(mock_read_file_and_write_config):
    """
    Passes test if `from_config(CONFIG_NAME)` returns `CONFIG_TASK`.
    """
    assert Task.from_config(CONFIG_NAME) == CONFIG_TASK


def test_arguments(monkeypatch):
    """
    Passes test if `Task.arguments` returns valid arguments.
    """
    scripts_dir = Path("scripts_dir")
    mocked_script_handler = MagicMock()
    mocked_script_handler.directory = scripts_dir
    monkeypatch.setattr(
        "ScriptRunner.taskhandler.script_handler",
        mocked_script_handler,
    )
    assert CONFIG_TASK.arguments == [
        *CONFIG_TASK.language_args,
        scripts_dir / CONFIG_TASK.script,
        *CONFIG_TASK.script_args,
    ]
