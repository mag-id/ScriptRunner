"""
`FileHandler` class and it's `config_handler` and `script_handler`
instances for workinng with configs and scripts directories.
"""

from os import walk
from pathlib import Path
from typing import List

from config import CONFIG_DIRECTORY, SCRIPT_DIRECTORY

__all__ = ["config_handler", "script_handler"]


class FileHandler:
    """
    Class for handllig files in specific `directory`.
    """

    def __init__(self, directory: Path):
        self.__dir = directory

    @property
    def directory(self) -> Path:
        """
        Returns specified directory.
        """
        return self.__dir

    @property
    def file_names(self) -> List[str]:
        """
        Returns file names from directory.
        """
        _, _, names = next(walk(self.__dir))
        return names

    def read_file(self, name: str, encoding: str = "utf-8") -> str:
        """
        Returns file content according to `name` (by default `encoding` is `"utf-8"`).
        """
        with open(file=self.__dir / name, mode="r", encoding=encoding) as file:
            return file.read()

    def write_file(self, name: str, content: str, encoding: str = "utf-8"):
        """
        Takes file `name` and `content`, writes it to the `directory`
        (by default `encoding` is `"utf-8"`).
        """
        with open(file=self.__dir / name, mode="w", encoding=encoding) as file:
            file.write(content)


config_handler = FileHandler(Path(CONFIG_DIRECTORY))
script_handler = FileHandler(Path(SCRIPT_DIRECTORY))
