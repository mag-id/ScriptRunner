"""
Unit tests for `ScriptRunner.prototype`.
"""

import pytest
from prototype import Task, get_tasks_queue, run_shell

CONFIG = """{
    "priority": 1,
    "arguments": ["echo", "script"],
    "failures": "stop",
    "next_config": false
}"""
TASK = Task(1, ["echo", "script"], "stop", False)


@pytest.fixture
def config(tmpdir):
    config_file = tmpdir.mkdir("configs").join("config.json")
    config_file.write_text(CONFIG, encoding="utf-8")
    return config_file


class TestTask:
    """Wraps tests for `Task`."""

    @staticmethod
    def test_from_config(config):
        Task.from_config(config) == TASK

    @staticmethod
    def test_next_task_yes(config):
        task = Task(
            priority=2,
            arguments=["echo", "script"],
            failures="stop",
            next_config=config,
        )
        assert task.next_task == TASK

    @staticmethod
    def test_next_task_no():
        task = Task(
            priority=2,
            arguments=["echo", "script"],
            failures="stop",
            next_config=False,
        )
        assert task.next_task is False


class TestGetTasksQueue:
    """Wraps tests for `get_tasks_queue`."""

    @staticmethod
    def test_initialization():
        queue = get_tasks_queue([TASK])
        assert queue.get() == TASK


class TestRunShell:
    """Wraps tests for `get_tasks_queue`."""

    @staticmethod
    def test_initialization():
        message = "script"
        out, err = run_shell(["echo", message])
        assert (out.strip(), err) == (message, "")
