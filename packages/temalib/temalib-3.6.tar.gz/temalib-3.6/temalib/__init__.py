import codecs
import os
from typing import Any

"""
a library that was made for working with files
"""

__author__ = "tema5002 <tema5002@gmail.com>"
__version__ = "3.6"
__license__ = "MIT"
__copyright__ = "2024, tema5002"
__short_description__ = "a library that works with files i guess"


def smthfile(fp: str, mode: str) -> codecs.StreamReaderWriter:
    """
    Opens a text file with UTF-8 encoding at the specified path (``fp``) with specified opening mode (``mode``)

    Note:
        Use ``openfile()`` for ``r`` reading mode and ``editfile()`` for ``w``

    Args:
        fp (str): The filepath of the text file to open.
        mode (str): The opening mode for the file.
                    (List of opening modes: https://docs.python.org/3/library/functions.html#open)

    Returns:
        codecs.StreamReaderWriter: A file object opened with UTF-8 encoding.

    Raises:
        OSError: If the file cannot be opened at the specified path.
    """
    return codecs.open(fp, mode, encoding="utf-8")


def openfile(fp: str) -> codecs.StreamReaderWriter:
    return smthfile(fp, "r")


def editfile(fp: str) -> codecs.StreamReaderWriter:
    return smthfile(fp, "w")


def get_folder_path(caller: str, *args: str, create_folders: bool = True) -> str:
    """
    Construct a folder path relative to the caller's directory, optionally creating missing folders.

    Args:
        caller (str): The path of the caller file (usually ``__file__``).
        args (str): One or more sub-folder names to be added to the path.
        create_folders (bool): Whether to create missing folders in the path. True by default.

    Returns:
        str: The constructed folder path.

    Raises:
        OSError: If there are errors creating folders (e.g., permission issues).
    """
    folder_dir = os.path.dirname(caller)
    for f in args:
        folder_dir = os.path.join(folder_dir, f)
        if create_folders and not os.path.exists(folder_dir):
            try:
                os.makedirs(folder_dir)
            except OSError as err:
                raise OSError(f"Failed to create folders: {err}") from err

    return folder_dir


def get_file_path(caller: str, *args: str, create_folders: bool = True, create_file: bool | str = "") -> str:
    """
    Constructs a file path relative to the ``caller``'s directory,
    optionally creating missing folders and the file itself.

    Args:
        caller: The path of the caller file (usually ``__file__``).
        args: One or more sub-folder names and the final file name to be added to the path.
        create_folders: Whether to create missing folders in the path. Defaults to True.
        create_file: The content to write to the file if it doesn't exist. Defaults to an empty string (``""``).
                     Set to ``False`` if you don't want the file to be created automatically.

    Return:
        The constructed file path.

    Raises:
        TypeError: If non-str values are passed as sub-folder names or file name in ``args``.
        OSError: If there are errors creating folders (e.g., permission issues).
    """

    folder_dir = get_folder_path(caller, *args[:-1], create_folders=create_folders)
    filepath = os.path.join(folder_dir, args[-1])

    if create_file is not False and not os.path.exists(filepath):
        editfile(filepath).write(create_file)

    return filepath


def add_line(fp: str, line: str) -> None:
    """
    Appends a line of text to the end of a file.

    Args:
        fp (str): The filepath of the text file to modify.
        line (str): The line of text to append to the file.

    Raises:
        OSError: If there are issues opening or writing to the file (e.g., permission issues).
    """
    with smthfile(fp, "a+") as f:
        f.seek(0)
        if f.read():
            line = "\n" + line
        f.write(line)


def remove_line(fp: str, line: str) -> None:
    """
    Removes a specific line of text from a file, if it exists.

    Args:
        fp (str): The filepath of the text file to modify.
        line (str): The exact line of text to remove from the file.

    Raises:
        OSError: If there are issues opening or writing to the file (e.g., permission issues).
    """
    file = openfile(fp).read().split("\n")
    file.remove(line)
    editfile(fp).write("\n".join(file))


def listpaths(fp: str) -> list[str]:
    """
    Retrieves a list of file paths within a specified directory.

    Args:
        fp (str): The path to the directory for which you want to list file paths.

    Returns:
        list[str]: A list containing the complete file paths for all files within the directory.

    Raises:
        OSError: If there's an issue accessing the directory (e.g., permission issues).
    """
    return [os.path.join(fp, i) for i in os.listdir(fp)]


def generate_ip(name: str) -> str:
    import random
    random.seed(name)
    return ".".join([str(random.randint(0, 255)) for _ in range(4)])
