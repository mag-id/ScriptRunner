"""Task dataclass."""

from dataclasses import dataclass
from json import loads
from typing import List

from filehandler import config_handler, script_handler


@dataclass(frozen=True, order=True)
class Task:
    """
    `Dataclass` for tasks handling.

    Attributes:
    -----------
    + `priority` - Integer represents task priority.
    + `script` - String name of the script.
    + `arguments` - List of strings represents script arguments.
    + `failures` - Strings with `pipeline` scpecific keyworks for exception processing.
    + `next_config` - String with name of the script config for next execution.

    Methods:
    --------
    + `from_config` - Returns `Task` instance from config file `name`.

    Properties:
    -----------
    + `next_task` - Returns `Task` instance from `Task.next_config`.
    If `Task.next_config` is `False` - returns `False`.

    + `command` - Returns command for Python shell script.

    """

    priority: int
    script: str
    arguments: List[str]
    failures: str
    next_config: str or False

    @classmethod
    def from_config(cls, name: str) -> "Task":
        """
        Returns `Task` instance from config file `name`.
        """
        return Task(**loads(config_handler.read_file(name)))

    @property
    def next_task(self) -> "Task" or False:
        """
        Returns `Task` instance from `Task.next_config`.
        If `Task.next_config` is `False` - returns `False`.
        """
        return Task.from_config(self.next_config) if self.next_config else False

    @property
    def command(self) -> List[str]:
        """
        Returns command for Python shell script.
        """
        return ["python", script_handler.directory / self.script, *self.arguments]
