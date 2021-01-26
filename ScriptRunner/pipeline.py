"""
Task priority queue pipeline.
"""

from queue import PriorityQueue
from subprocess import run
from typing import List, Tuple

from exceptions import StopKeywordFailures, UnknownKeywordFailures
from filehandler import config_handler
from taskhandler import Task

SKIP = "skip"
STOP = "stop"
UNKNOWN_KEYWORD_MESSAGE = "Unknown `'failures'` keyword, check config file."


def submit_tasks():
    """
    Converts all configs to tasks and submits them to the tasks queue.
    """
    tasks = [Task.from_config(name) for name in config_handler.file_names]
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
    Runs while loop and execute tasks from `task_queue`.
    """
    while not tasks_queue.empty():
        execute_task(tasks_queue.get())


def execute_task(task: Task):
    """
    Executes `task` and prints `task`
    with `stdout` and `stderr`.
    """
    stdout, stderr = run_shell(task.arguments)

    print(task)
    print(stdout)
    print(stderr)

    if stderr:
        handle_failure(task.failures)

    next_task = task.next_task

    if next_task:
        execute_task(next_task)


def handle_failure(failure: str):
    """
    Process exceptions according to keywords:
    + if `"skip"` - skip exception and go to the next task;
    + if `"stop"` - raise `StopScriptRunnerExc` and stop tasks queue execution;
    Also prints the keyword.

    If unknown keyword passed - raises
    `UnknownKeywordFailures(UNKNOWN_KEYWORD_MESSAGE)`.
    """
    if failure == STOP:
        print(STOP)
        raise StopKeywordFailures
    elif failure == SKIP:
        print(SKIP)
    else:
        raise UnknownKeywordFailures(UNKNOWN_KEYWORD_MESSAGE)


# https://docs.python.org/3.8/library/subprocess.html
def run_shell(arguments: List[str]) -> Tuple[str, str]:
    """
    Runs `arguments` in the shell and returns `stdout` and `stderr` as text.
    """
    catched = run(args=arguments, shell=False, capture_output=True, text=True)
    return catched.stdout, catched.stderr
