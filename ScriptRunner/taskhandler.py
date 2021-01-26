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
    + `language_args` - List of strings with language arguments.
    + `script` - String name of the script.
    + `script_args` - List of strings with script arguments.
    + `failures` - Strings with `pipeline` scpecific keyworks for exception processing.
    + `next_config` - String with name of the script config for next execution.

    Methods:
    --------
    + `from_config` - Returns `Task` instance from config file `name`.

    Properties:
    -----------
    + `next_task` - Returns `Task` instance from `Task.next_config`.
    If `Task.next_config` is `False` - returns `False`.

    + `arguments` - Returns shell arguments.

    """

    priority: int
    language_args: List[str]
    script: str
    script_args: List[str]
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
    def arguments(self) -> List[str]:
        """
        Returns shell arguments.
        """
        return [
            *self.language_args,
            script_handler.directory / self.script,
            *self.script_args,
        ]
