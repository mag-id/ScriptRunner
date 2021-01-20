"""
Финальный проект - запускатель скриптов на сервере с вэб-интерфейсом.

1. Приложение стартует на (удалённой) машине,
в конфигурации указана папка, в которой будут находиться
скрипты для запуска и папка с конфигурациями для этих скриптов.
Если есть скрипты без конфигов, то приложение их не трогает.

2. В конфигурации можно указать:
  * параметры для запуска
  * приоритет запуска
  * что делать, если скрипт завершится с ошибкой
  * какой скрипт запустить следующим
  (до запуска цепочки скриптов нужно проверить, что для всех есть конфигурация)

3. Форма для редактирования конфигурации скрипта.
"""
from dataclasses import dataclass
from json import load
from queue import PriorityQueue
from subprocess import run
from typing import List, Tuple

SKIP = "SKIP"
STOP = "STOP"


@dataclass(frozen=True, order=True)
class Task:
    """
    `Dataclass` for task configuration handling.

    Attributes:
    -----------
    + `priority` - Integer Represents task priority.
    + `arguments` - List of strings represents shell arguments.
    + `failures` - Keyword:

    if `"SKIP"` - skip and go to the next task;

    if `"STOP"` - stop tasks queue execution;

    + `next_config` - String with path to the script config for next execution.

    Methods:
    --------
    + `from_config` - Returns `Task` instance from `path` to the config file.
    By default `encoding` is `"utf-8"`.

    Properties:
    -----------
    + `next_task` - Returns `Task` instance from `task.next_config`.
    If `task.next_config` is `False` - returns `False`.
    """

    priority: int
    arguments: List[str]
    failures: SKIP or STOP
    next_config: str or False

    @classmethod
    def from_config(cls, path: str, encoding: str = "utf-8") -> "Task":
        """
        Returns `Task` instance from `path` to the config file.
        By default `encoding` is `"utf-8"`.
        """
        with open(file=path, mode="r", encoding=encoding) as file:
            return Task(**load(file))

    @property
    def next_task(self) -> "Task" or False:
        """
        Returns `Task` instance from `task.next_config`.
        If `task.next_config` is `False` - returns `False`.
        """
        return Task.from_config(self.next_config) if self.next_config else False


def submit(configs: List[str]):
    """
    Converts `configs` to `tasks` and submits
    them to the `tasks_queue` for execution.
    """
    tasks = list(map(Task.from_config, configs))
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
    stdout, stderr = run_shell(task.arguments)

    if stdout:  # TODO: logging ?
        print(stdout)

    if stderr:  # TODO: logging ?
        print(stderr)
        handle_failure(task.failures)

    next_task = task.next_task
    if next_task:
        execute_task(next_task)


"""
def log_to_file(content: str, path: str, encoding: str = "utf-8"):
    # TODO
    with open(file=path, mode="a", encoding=encoding) as file:
        file.write(content)
"""


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
def run_shell(arguments: List[str]) -> Tuple[str, str]:
    """
    Runs `arguments` in the shell and returns `stdout` and `stderr` as text.
    """
    catched = run(args=arguments, shell=False, capture_output=True, text=True)
    return catched.stdout, catched.stderr


if __name__ == "__main__":
    submit(
        [
            "data/configs/first_config.json",
            "data/configs/second_config.json",
        ]
    )
