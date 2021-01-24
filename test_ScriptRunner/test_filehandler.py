"""Unit tests for `FileHandler` from `ScriptRunner.filehandler`."""

from ScriptRunner.filehandler import FileHandler


class TestFIleNames:
    """Wraps tests for `FileHandler.file_names`."""

    @staticmethod
    def test_empty(test_dir):
        """
        Passes test if `FIleNames.file_names` is empty.
        """
        handler = FileHandler(test_dir)
        assert handler.file_names == []

    @staticmethod
    def test_one_file(test_dir, test_file):
        """
        Passes test if `FIleNames.file_names` contains `"one.txt"`.
        """
        handler = FileHandler(test_dir)
        test_file(filename="one.txt", content="")
        assert handler.file_names == ["one.txt"]

    @staticmethod
    def test_two_file(test_dir, test_file):
        """
        Passes test if `FileHandler.file_names` contains `"one.txt"` and `"two.txt"`.
        """
        handler = FileHandler(test_dir)
        test_file(filename="one.txt", content="")
        test_file(filename="two.txt", content="")
        assert set(handler.file_names) == set(["one.txt", "two.txt"])


def test_directory(test_dir):
    """
    Passes test if `FileHandler.directory` is equal to `test_dir`.
    """
    handler = FileHandler(test_dir)
    assert handler.directory == test_dir


def test_write_file(test_dir):
    """
    Passes test if file `"to_write.txt"` with
    `"content"` correctly writed into the `test_dir`.
    """
    filename, content = "to_write.txt", "content"

    handler = FileHandler(test_dir)
    handler.write_file(filename, content)

    with open(file=test_dir / filename, mode="r", encoding="utf-8") as file:
        assert file.read() == content


def test_read_file(test_dir, test_file):
    """
    Passes test if file `"to_read.txt"` with
    `"content"` correctly readed from the `test_dir`.
    """
    filename, content = "to_read.txt", "content"

    handler = FileHandler(test_dir)
    test_file(filename, content)

    assert handler.read_file(filename) == content
