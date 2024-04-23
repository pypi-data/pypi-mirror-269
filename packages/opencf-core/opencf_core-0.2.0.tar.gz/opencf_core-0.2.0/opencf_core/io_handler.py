"""
Input/Output Handler Module

This module is designed to provide a structured approach to handling file input and output operations across various
formats such as plain text, CSV, JSON, and potentially XML. It introduces a set of abstract base classes and concrete
implementations for reading from and writing to files, ensuring type safety and format consistency through method
signatures and runtime checks.
"""

import csv
import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List


class FileReader(ABC):
    """
    Abstract base class for file readers.
    """

    input_format: type = None

    @abstractmethod
    def _check_input_format(self, content: Any) -> bool:
        """
        Checks if the provided content matches the expected input format.

        Args:
            content (Any): The content to be checked.

        Returns:
            bool: True if the content matches the expected input format, False otherwise.
        """
        pass

    @abstractmethod
    def _read_content(self, input_path: Path) -> Any:
        """
        Reads and returns the content from the given input path.

        Args:
            input_path (Path): The path to the input file.

        Returns:
            Any: The content read from the input file.
        """
        pass


class FileWriter(ABC):
    """
    Abstract base class for file writers.
    """

    output_format = None

    @abstractmethod
    def _check_output_format(self, content: Any) -> bool:
        """
        Checks if the provided content matches the expected output format.

        Args:
            content (Any): The content to be checked.

        Returns:
            bool: True if the content matches the expected output format, False otherwise.
        """
        pass

    @abstractmethod
    def _write_content(self, output_path: Path, output_content: Any):
        """
        Writes the provided content to the given output path.

        Args:
            output_path (Path): The path to the output file.
            output_content (Any): The content to be written to the output file.
        """
        pass


class SamePathReader(FileReader):
    """
    A FileReader that returns the input path itself, useful for operations where the file path is the desired output.
    """

    input_format = Path

    def _check_input_format(self, content: Path):
        return isinstance(content, Path)

    def _read_content(self, input_path: Path) -> Path:
        return input_path


class TxtToStrReader(FileReader):
    """
    Reads content from a text file and returns it as a string.
    """

    input_format = str

    def _check_input_format(self, content: str):
        return isinstance(content, str)

    def _read_content(self, input_path: Path) -> str:
        return input_path.read_text()


class StrToTxtWriter(FileWriter):
    """
    Writes a string to a text file.
    """

    output_format = str

    def _check_output_format(self, content: str):
        return isinstance(content, str)

    def _write_content(self, output_path: Path, output_content: str):
        output_path.write_text(output_content)


class CsvToListReader(FileReader):
    """
    Reads content from a CSV file and returns it as a list of lists, where each sublist represents a row.
    """

    input_format = List[List[str]]

    def _check_input_format(self, content: List[List[str]]):
        return isinstance(content, list) and all(
            isinstance(row, list) for row in content
        )

    def _read_content(self, input_path: Path) -> List[List[str]]:
        with open(input_path, "r", newline="") as csvfile:
            reader = csv.reader(csvfile)
            return [row for row in reader]


class ListToCsvWriter(FileWriter):
    """
    Writes content as a list of lists to a CSV file, where each sublist represents a row.
    """

    output_format = List[List[str]]

    def _check_output_format(self, content: List[List[str]]):
        return isinstance(content, list) and all(
            isinstance(row, list) for row in content
        )

    def _write_content(self, output_path: Path, output_content: List[List[str]]):
        with open(output_path, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            for row in output_content:
                writer.writerow(row)


class JsonToDictReader(FileReader):
    """
    Reads content from a JSON file and returns it as a dictionary.
    """

    input_format = Dict[str, Any]

    def _check_input_format(self, content: Dict[str, Any]):
        return isinstance(content, dict)

    def _read_content(self, input_path: Path) -> Dict[str, Any]:
        return json.loads(input_path.read_text())


class DictToJsonWriter(FileWriter):
    """
    Writes content from a dictionary to a JSON file.
    """

    output_format = Dict[str, Any]

    def _check_output_format(self, content: Dict[str, Any]):
        return isinstance(content, dict)

    def _write_content(self, output_path: Path, output_content: Dict[str, Any]):
        return output_path.write_text(json.dumps(output_content))


class XmlToStrReader(FileReader):
    """
    Reads content from an XML file and returns it as a string.
    """

    input_format = str

    def _check_input_format(self, content: str):
        # Add your XML validation logic here
        return isinstance(content, str)

    def _read_content(self, input_path: Path) -> str:
        return input_path.read_text()


class StrToXmlWriter(FileWriter):
    """
    Writes content as a string to an XML file.
    """

    output_format = str

    def _check_output_format(self, content: str):
        # Add your XML validation logic here
        return isinstance(content, str)

    def _write_content(self, output_path: Path, output_content: str):
        output_path.write_text(output_content)
