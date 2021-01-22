"""
TODO
"""
from abc import ABC
from dataclasses import dataclass
from json import loads
from queue import PriorityQueue
from subprocess import run
from typing import List, Tuple

from filehandler import config_handler, script_handler

SKIP = "SKIP"
STOP = "STOP"


@dataclass(frozen=True, order=True)
class Task(ABC):
    priority: int

    @property
    def command(self):
        raise NotImplementedError


@dataclass(frozen=True, order=True)
class PythonTask(Task):
    """
    TODO
    `Dataclass` for Python tasks handling.

    Attributes:
    -----------
    + `priority` - Integer Represents Python task priority.
    + `script` - String name of the Python script.
    + `arguments` - List of strings represents Python script arguments.
    + `failures` - Keyword:

    if `"SKIP"` - skip and go to the next task;

    if `"STOP"` - stop tasks queue execution;

    + `next_config` - String with path to the Python script config for next execution.

    Methods:
    --------
    + `from_config` - Returns `PythonTask` instance from config file `name`.

    Properties:
    -----------
    + `next_task` - Returns `PythonTask` instance from `PythonTask.next_config`.
    If `PythonTask.next_config` is `False` - returns `False`.

    + `command`
    """

    script: str
    arguments: List[str]
    failures: SKIP or STOP
    next_config: str or False

    @classmethod
    def from_config(cls, name: str) -> "PythonTask":
        """
        Returns `PythonTask` instance from config file `name`.
        """
        return PythonTask(**loads(config_handler.read_file(name)))

    @property
    def next_task(self) -> "PythonTask" or False:
        """
        Returns `PythonTask` instance from `python_task.next_config`.
        If `python_task.next_config` is `False` - returns `False`.
        """
        return PythonTask.from_config(self.next_config) if self.next_config else False

    @property
    def command(self) -> List[str]:
        """
        Returns shell arguments.
        """
        return ["python", script_handler.directory / self.script, *self.arguments]


def submit_python_queue():
    """
    TODO:
    Converts all `configs` to `PythonTask`s and submits
    them to the `tasks_queue` for execution.
    """
    tasks = list(map(PythonTask.from_config, config_handler.file_names))
    execute_tasks_queue(get_tasks_queue(tasks))


def get_tasks_queue(tasks: List[Task]) -> PriorityQueue:
    """
    Returns priority queue of the `tasks` according to `Task.priority`.
    """
    queue = PriorityQueue()
    for task in tasks:
        queue.put(task)
    return queue


def execute_tasks_queue(tasks_queue: PriorityQueue):
    """
    Runs while loop and `execute_task`s from `task_queue`.
    """
    while not tasks_queue.empty():
        execute_task(tasks_queue.get())


def execute_task(task: Task):
    """
    TODO
    """
    stdout, stderr = run_shell(task.command)

    if stdout:  # TODO: logging ?
        print(stdout)

    if stderr:  # TODO: logging ?
        print(stderr)
        handle_failure(task.failures)

    next_task = task.next_task
    if next_task:
        execute_task(next_task)


def handle_failure(failure: str):
    """
    TODO
    """
    if failure == SKIP:
        pass

    if failure == STOP:
        raise Exception(STOP)


# https://www.youtube.com/watch?v=2Fp1N6dof0Y
# https://docs.python.org/3.8/library/subprocess.html
def run_shell(command: List[str]) -> Tuple[str, str]:
    """
    Runs `command` in the shell and returns `stdout` and `stderr` as text.
    """
    catched = run(args=command, shell=False, capture_output=True, text=True)
    return catched.stdout, catched.stderr
