"""
`FileHandler` class and it's `config_handler` and `script_handler`
instances for workinng with configs and scripts directories.
"""

from base64 import b64decode
from os import remove, walk
from pathlib import Path
from typing import List

__all__ = ["config_handler", "script_handler"]


class FileHandler:
    def __init__(self, directory: Path):
        self.__dir = directory

    @property
    def directory(self) -> Path:
        return self.__dir

    @property
    def file_names(self) -> List[str]:
        _, _, names = next(walk(self.__dir))
        return names

    def read_file(self, name: str, encoding: str = "utf-8") -> str:
        with open(file=self.__dir / name, mode="r", encoding=encoding) as file:
            return file.read()

    def write_file(self, name: str, content: str, encoding: str = "utf-8"):
        with open(file=self.__dir / name, mode="w", encoding=encoding) as file:
            file.write(content)

    def write_uploaded_file(self, name: str, content: str):
        _type, encoded_string = content.split(",")
        decoded_string = b64decode(encoded_string)
        with open(file=self.__dir / name, mode="wb") as file:
            file.write(decoded_string)

    def delete_file(self, name: str):
        remove(path=self.__dir / name)


config_handler = FileHandler(Path("ScriptRunner/data/configs"))
script_handler = FileHandler(Path("ScriptRunner/data/scripts"))
