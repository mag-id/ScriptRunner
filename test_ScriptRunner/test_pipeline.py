"""
Unit tests for `execute_task`, `handle_failure`,
and `run_shell` from `ScriptRunner.pipeline`.
"""
from unittest.mock import MagicMock

import pytest
from exceptions import StopKeywordFailures, UnknownKeywordFailures
from pipeline import (
    SKIP,
    STOP,
    UNKNOWN_KEYWORD_MESSAGE,
    execute_task,
    handle_failure,
    run_shell,
)


class TestHandleFailure:
    """Wraps tests for `handle_failure`."""

    @staticmethod
    def test_stop(capsys):
        """
        Passes test if `handle_failure(STOP)` raises
        `StopKeywordFailures` and prints to stdout `STOP`.
        """
        with pytest.raises(StopKeywordFailures):
            handle_failure(STOP)
        out, err = capsys.readouterr()
        assert out.rstrip("\n") == STOP

    @staticmethod
    def test_skip(capsys):
        """
        Passes test if `handle_failure(SKIP)` prints to stdout `SKIP`.
        """
        handle_failure(SKIP)
        out, err = capsys.readouterr()
        assert out.rstrip("\n") == SKIP

    @staticmethod
    def test_unknown_keyword():
        """
        Passes test if `handle_failure` with unknown keyword
        raises `UnknownKeywordFailures(UNKNOWN_KEYWORD_MESSAGE)`.
        """
        with pytest.raises(UnknownKeywordFailures, match=UNKNOWN_KEYWORD_MESSAGE):
            handle_failure("something_unknown")


# TODO: test_execute_task
# See `execute_task` comment, if realisation will be separated it will be more testable.
# Also, the test can be simplified using fixtures.
def test_execute_task(monkeypatch, capsys, test_file):
    """
    Generates python script, executes with mocked task
    and checks that:

    + strerr is empty;
    + stdout contains printed task;
    + stdout contains printed script message;
    + stdout contains script exception;
    + stdout contains `SKIP` keyword.
    """
    # Generates the python script with print and exception.
    message = "pyscript message"
    exception = "pyscript exception"
    filename = "pyscript.py"
    content = f"print('{message}')\nraise Exception('{exception}')"
    pyscript = test_file(filename, content)

    # Mocks `Task` instance.
    mocked_task = MagicMock()
    mocked_task.arguments = ["python", pyscript]
    mocked_task.failures = SKIP
    mocked_task.next_task = False

    # Executes.
    execute_task(mocked_task)

    # Catches stdout, stderr.
    out, err = capsys.readouterr()

    assert err == ""
    assert str(mocked_task) in out
    assert message in out
    assert exception in out
    assert SKIP in out


def test_run_shell():
    """
    Passes test if `run_shell` executes `echo` command.
    """
    test_message = "test message"
    out, err = run_shell(["echo", test_message])
    assert (out.rstrip("\n"), err) == (test_message, "")
