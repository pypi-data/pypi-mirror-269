"""A service for interacting with the filesystem."""

import json
import os
from typing import List

import structlog

LOGGER = structlog.get_logger(__name__)


class FileService:
    """A service for interacting with the filesystem."""

    @staticmethod
    def write_windows_install_paths(target_file: str, paths: List[str]) -> None:
        """
        Write the given list of paths to the target file.

        :param target_file: File to write paths to.
        :param paths: Paths to write to file.
        """
        with open(target_file, "a") as out:
            if os.stat(target_file).st_size > 0:
                out.write(os.pathsep)
            out.write(os.pathsep.join(paths))

        LOGGER.info(f"Finished writing binary paths on Windows to {target_file}")

    @staticmethod
    def append_lines_to_file(file_name: str, content: List[str]) -> None:
        """
        Append the given content to the specified file.

        :param file_name: File to write to.
        :param content: Content to write to file.
        """
        with open(file_name, "a") as out:
            out.write("\n".join(content))

    @staticmethod
    def delete_file(file_name: str) -> None:
        """
        Delete the given file from the filesystem.

        :param file_name: File to delete.
        """
        os.remove(file_name)

    @staticmethod
    def write_dict_to_json(file_name: str, content: dict) -> None:
        """
        Write the given dict to the specified file in json format.

        :param file_name: File to write to.
        :param content: Content to write to file.
        """
        with open(file_name, "w") as out:
            json.dump(content, out, indent=2)
