"""
File Type Definitions Module

This module provides a comprehensive framework for handling various file types within a file conversion context.
It defines classes and enumerations for identifying, validating, and working with different file types, based on
file extensions, MIME types, and optionally, file content. It also includes custom exceptions for handling common
errors related to file type processing.

Classes:
- UnsupportedFileTypeError: Custom exception for handling unsupported file types.
- EmptySuffixError: Specialized exception for cases where a file's suffix does not provide enough information
                    to determine its type.
- FileNotFoundError: Raised when a specified file does not exist.
- MismatchedException: Exception for handling cases where there's a mismatch between expected and actual file attributes.
- FileType: Enum class that encapsulates various file types supported by the system, providing methods for
            type determination from file attributes.

Functions:
- test_file_type_parsing(): Demonstrates and validates the parsing functionality for various file types.
- test_file_type_matching(): Tests the matching and validation capabilities of the FileType class.

Dependencies:
- collections.namedtuple: For defining simple classes for storing MIME type information.
- enum.Enum: For creating the FileType enumeration.
- pathlib.Path: For file path manipulations and checks.
- opencf_core.mimes.guess_mime_type_from_file: Utility function to guess MIME type from a file path.
"""

from collections import namedtuple
from enum import Enum
from pathlib import Path
from typing import Union

from .mimes import guess_mime_type_from_file


# Custom Exceptions
class UnsupportedFileTypeError(Exception):
    """Exception raised for handling cases of unsupported file types."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class EmptySuffixError(UnsupportedFileTypeError):
    """Exception raised when a file's suffix does not provide enough information to determine its type."""

    def __init__(self):
        self.message = "Filetype not parsed from empty suffix."
        super().__init__(self.message)


class FileNotFoundError(Exception):
    """Exception raised when the specified file cannot be found."""

    def __init__(self, file_path):
        self.file_path = file_path
        message = f"File '{file_path}' does not exist."
        super().__init__(message)


class MismatchedException(Exception):
    """Exception raised for mismatches between expected and actual file attributes."""

    def __init__(self, label, claimed_val, expected_vals):
        super().__init__(
            f"Mismatched {label}: Found '{claimed_val}', Expected one of '{expected_vals}'"
        )


# File Type and MIME Type Definitions
MimeType = namedtuple(
    "MimeType", ["extensions", "mime_types", "upper_mime_types"], defaults=[(), (), ()]
)


class FileType(Enum):
    """Enumeration of supported file types with methods for type determination and validation."""

    # Enum members defined with their respective MIME type information
    NOTYPE = MimeType()
    CSV = MimeType(("csv",), ("text/csv",))
    EXCEL = MimeType(
        ("xls", "xlsx"),
        (
            "application/vnd.ms-excel",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        ),
    )
    MSWORD = MimeType(
        ("docx", "doc"),
        (
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "application/msword",
        ),
    )
    JSON = MimeType(("json",), ("application/json",))
    PDF = MimeType(("pdf",), ("application/pdf",))
    IMAGE = MimeType(("jpg", "jpeg", "png"), ("image/jpeg", "image/png"))
    GIF = MimeType(("gif",), ("image/gif",))
    VIDEO = MimeType(("mp4", "avi"), ("video/mp4", "video/x-msvideo"))
    XML = MimeType(("xml",), ("application/xml", "text/xml"))
    MARKDOWN = MimeType(("md",), ("text/markdown",), ("text/plain",))
    TEXT = MimeType(
        ("txt",), ("text/plain",)
    )  # put it at bottom as many other filetypes may be marked as text/plain too
    UNHANDLED = MimeType()

    @classmethod
    def from_suffix(cls, suffix: str, raise_err: bool = False):
        """
        Determines a FileType from a file's suffix.

        Args:
            suffix (str): The file suffix (extension).
            raise_err (bool, optional): Whether to raise an exception if the type is unhandled. Defaults to False.

        Returns:
            FileType: The determined FileType enumeration member.

        Raises:
            EmptySuffixError: If the suffix is empty and raise_err is True.
            UnsupportedFileTypeError: If the file type is unhandled and raise_err is True.
        """
        suffix = suffix.lower().lstrip(".")
        if not suffix:
            if raise_err:
                raise EmptySuffixError()
            else:
                return cls.NOTYPE
        for member in cls:
            if member.value.extensions and suffix in member.value.extensions:
                return member

        if raise_err:
            raise UnsupportedFileTypeError(f"Unhandled filetype from suffix={suffix}")
        else:
            return cls.UNHANDLED

    @classmethod
    def from_mimetype(cls, file_path: Union[str, Path], raise_err: bool = False):
        """
        Determines a FileType from a file's MIME type.

        Args:
            file_path (str): The path to the file.
            raise_err (bool, optional): Whether to raise an exception if the type is unhandled. Defaults to False.

        Returns:
            FileType: The determined FileType enumeration member.

        Raises:
            FileNotFoundError: If the file does not exist.
            UnsupportedFileTypeError: If the file type is unhandled and raise_err is True.
        """

        file = Path(file_path)

        if not file.exists():
            raise FileNotFoundError(file_path)

        file_mimetype = guess_mime_type_from_file(str(file))

        for member in cls:
            if member.value.mime_types and file_mimetype in member.value.mime_types:
                return member

        if raise_err:
            raise UnsupportedFileTypeError(
                f"Unhandled filetype from mimetype={file_mimetype}"
            )
        else:
            return cls.UNHANDLED

    # @classmethod
    # def from_content(cls, path: Path, raise_err=False):
    #     file_path = Path(path)
    #     file_type = get_file_type(file_path)['f_type']
    #     # logger.info(file_type)
    #     return file_type #text/plain, application/json, text/xml, image/png, application/csv, image/gif, ...
    #     member = cls.UNHANDLED
    #     return member

    @classmethod
    def from_path(cls, path: Path, read_content=False, raise_err=False):
        """
        Determines the FileType of a file based on its path. Optionally reads the file's content to verify its type.

        Args:
            path (Path): The path to the file.
            read_content (bool, optional): If True, the method also checks the file's content to determine its type.
                                           Defaults to False.
            raise_err (bool, optional): If True, raises exceptions for unsupported types or when file does not exist.
                                        Defaults to False.

        Returns:
            FileType: The determined FileType enumeration member based on the file's suffix and/or content.

        Raises:
            FileNotFoundError: If the file does not exist when attempting to read its content.
            UnsupportedFileTypeError: If the file type is unsupported and raise_err is True.
            AssertionError: If there is a mismatch between the file type determined from the file's suffix and its content.
        """
        file_path = Path(path)

        raise_err1 = raise_err and (not read_content)
        raise_err2 = raise_err

        # get member from suffix
        member1 = cls.from_suffix(file_path.suffix, raise_err=raise_err1)

        # if we're not checking the file content, return
        if not read_content:
            return member1

        # the file should exists for content reading
        if not file_path.exists():
            raise FileNotFoundError(f"File '{file_path}' does not exist.")

        # get member from content
        member2 = cls.from_mimetype(file_path, raise_err=raise_err2)

        # if suffix didnt give a filetype, use the one from content
        if not member1.is_true_filetype():
            return member2

        assert (
            member1 == member2
        ), f"file type from suffix ({member1}) mismatch with filepath from path({member2})"

        return member1

    def is_true_filetype(self):
        """
        Determines if the FileType instance represents a supported file type based on the presence of defined extensions.

        Returns:
            bool: True if the FileType has at least one associated file extension, False otherwise.
        """
        return len(self.value.extensions) != 0

    def get_suffix(self):
        """
        Retrieves the primary file extension associated with the FileType.

        Returns:
            str: The primary file extension for the FileType, prefixed with a period.
                 Returns an empty string if the FileType does not have an associated extension.
        """
        ext = self.value.extensions[0] if self.is_true_filetype() else ""
        return f".{ext}"

    def is_valid_suffix(self, suffix: str, raise_err=False):
        """
        Validates whether a given file extension matches the FileType's expected extensions.

        Args:
            suffix (str): The file extension to validate, including the leading period (e.g., ".txt").
            raise_err (bool, optional): If True, raises a MismatchedException for invalid extensions.
                                        Defaults to False.

        Returns:
            bool: True if the suffix matches one of the FileType's extensions, False otherwise.

        Raises:
            MismatchedException: If the suffix does not match and raise_err is True.
        """
        _val = FileType.from_suffix(suffix=suffix)
        is_valid = _val == self
        if raise_err and not is_valid:
            raise MismatchedException(f"suffix ({suffix})", _val, self.value.extensions)
        return is_valid

    def is_valid_path(self, path: Path, raise_err=False, read_content=False):
        """
        Validates whether the file at a given path matches the FileType, optionally checking the file's content.

        Args:
            path (Path): The path to the file to validate.
            raise_err (bool, optional): If True, raises a MismatchedException for a mismatching file type.
                                        Defaults to False.
            read_content (bool, optional): If True, also validates the file's content type against the FileType.
                                           Defaults to False.

        Returns:
            bool: True if the file's type matches the FileType, based on its path and optionally its content.
                  False otherwise.

        Raises:
            MismatchedException: If the file's type does not match and raise_err is True.
        """
        _val = FileType.from_path(path, read_content=read_content)
        is_valid = _val == self
        if raise_err and not is_valid:
            raise MismatchedException(f"suffix/mime-type ({path})", _val, self.value)
        return is_valid

    def is_valid_mime_type(self, path: Path, raise_err=False):
        """
        Validates whether the MIME type of the file at the specified path aligns with the FileType's expected MIME types.

        This method first determines the FileType based on the file's actual MIME type (determined by reading the file's content)
        and then checks if this determined FileType matches the instance calling this method. Special consideration is given to
        FileType.TEXT, where a broader compatibility check is performed due to the generic nature of text MIME types.

        Args:
            path (Path): The path to the file whose MIME type is to be validated.
            raise_err (bool, optional): If True, a MismatchedException is raised if the file's MIME type does not match
                                        the expected MIME types of the FileType instance. Defaults to False.

        Returns:
            bool: True if the file's MIME type matches the expected MIME types for this FileType instance or if special
                compatibility conditions are met (e.g., for FileType.TEXT with "text/plain"). Otherwise, False.

        Raises:
            MismatchedException: If raise_err is True and the file's MIME type does not match the expected MIME types
                                for this FileType instance, including detailed information about the mismatch.
        """
        _val = FileType.from_mimetype(path)
        is_valid = _val == self

        # many things can be text/plain
        if _val == FileType.TEXT and "text/plain" in self.value.upper_mime_types:
            is_valid = True

        if raise_err and not is_valid:
            raise MismatchedException(
                f"content-type({path})", _val, self.value.mime_types
            )
        return is_valid


# Test Functions
def test_file_type_parsing():
    """Tests for validating the functionality of file type parsing."""
    # Test parsing of different file types
    text_path = Path("test.txt")
    csv_path = Path("data.csv")
    excel_path = Path("results.xlsx")
    json_path = Path("config.json")
    img_path = Path("picture.jpg")

    assert FileType.from_path(text_path) == FileType.TEXT
    assert FileType.from_path(csv_path) == FileType.CSV
    assert FileType.from_path(excel_path) == FileType.EXCEL
    assert FileType.from_path(json_path) == FileType.JSON
    assert FileType.from_path(img_path) == FileType.IMAGE
    assert FileType.from_path(Path("no_extension")) == FileType.NOTYPE
    assert FileType.from_path(Path("unknown.xyz")) == FileType.UNHANDLED


def test_file_type_matching():
    """Tests for validating the functionality of file type matching."""
    # Test matching of different file types
    text_path = Path("test.txt")
    csv_path = Path("data.csv")
    excel_path = Path("results.xlsx")
    json_path = Path("config.json")
    img_path = Path("picture.jpg")

    assert FileType.TEXT.is_valid_path(text_path)
    assert not FileType.TEXT.is_valid_path(csv_path)

    assert FileType.CSV.is_valid_path(csv_path)
    assert not FileType.CSV.is_valid_path(excel_path)

    assert FileType.EXCEL.is_valid_path(excel_path)
    assert not FileType.EXCEL.is_valid_path(json_path)

    assert FileType.JSON.is_valid_path(json_path)
    assert not FileType.JSON.is_valid_path(img_path)

    assert FileType.IMAGE.is_valid_path(img_path)
    assert not FileType.IMAGE.is_valid_path(text_path)

    assert FileType.NOTYPE.is_valid_path(Path("no_extension"))
    assert not FileType.NOTYPE.is_valid_path(text_path)

    assert FileType.UNHANDLED.is_valid_path(Path("unknown.xyz"))
    assert not FileType.UNHANDLED.is_valid_path(csv_path)


if __name__ == "__main__":
    import sys

    sys.path.append(".")
    test_file_type_parsing()
    test_file_type_matching()
    print("All tests passed!")
