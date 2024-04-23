"""
Base Converter Module

This module serves as a foundation for creating file conversion utilities. It facilitates the development
of file converters through abstract base classes, managing file types, and handling input and output files
efficiently. The module is designed to be extendible, supporting various file formats and conversion strategies.

Classes:
- ResolvedInputFile: Manages file paths and types, resolving them as needed.
- BaseConverter: An abstract base class for creating specific file format converters, enforcing the implementation
                 of file conversion logic.

Exceptions:
- ValueError: Raised when file paths or types are incompatible or unsupported.
- AssertionError: Ensured for internal consistency checks, confirming that file types match expected values.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Optional, Union

from .filetypes import EmptySuffixError, FileType
from .io_handler import FileReader, FileWriter, SamePathReader
from .logger import logger


class ResolvedInputFile:
    """
    Handles resolving the file type of a given file or folder, managing path adjustments and optional content reading.
    """

    def __init__(
        self,
        path: Union[str, Path],
        is_dir: Optional[bool] = None,
        should_exist: bool = True,
        file_type: Optional[str] = None,
        add_suffix: bool = False,
        read_content: bool = False,
    ):
        """
        Initializes an instance of ResolvedInputFile with options for type resolution and path modification.

        Args:
            path (str): The path to the file or folder.
            is_dir (bool, optional): Specifies if the path is a directory. If None, inferred using pathlib. Defaults to None.
            should_exist (bool, optional): Specifies if the existence of the path is required. Defaults to True.
            file_type (str, optional): The explicit type of the file. If None, attempts to resolve to a FileType object based on the path or content.
            add_suffix (bool, optional): Whether to append the resolved file type's suffix to the file path. Defaults to False.
            read_content (bool, optional): Whether to read the file's content to assist in type resolution. Defaults to False.
        """
        # Convert path to Path object
        self.path = Path(path)

        self._check_existence(should_exist)

        # Infer if the path is a directory
        if is_dir is None:
            is_dir = self._resolve_path_type(file_type=file_type)

        # Resolve the file type
        if is_dir:
            assert file_type, "file_type must be set when is_dir is activated"
            self.file_type, self.suffix = self._resolve_directory_type(file_type)
            self.is_dir = True
        else:
            self.file_type, self.suffix = self._resolve_file_type(
                file_type, read_content, add_suffix
            )
            self.is_dir = False

    def _resolve_path_type(self, file_type: Optional[str] = None) -> bool:
        """
        Determines if the provided path refers to a directory or a file, based on its existence, suffix, and file_type.

        Args:
            file_type (str, optional): The type of file expected at the path. Influences directory creation and type resolution.

        Returns:
            bool: True if the path is determined to be a directory, False if it is a file.
        """
        filesuffix_set = self.path.suffix != ""
        filetype_set = file_type is not None

        if self.path.exists():
            # Check if the existing path is a directory
            is_dir = self.path.is_dir()
            logger.debug(f"Path exists. Setting is_dir to {is_dir}.")
        elif not filesuffix_set and filetype_set:
            # If there's no suffix and a file_type is specified, assume it's a directory and create it
            self.path.mkdir(parents=False, exist_ok=True)
            is_dir = True
            logger.debug(
                "No suffix found and file_type is specified. Assuming directory and creating it. Setting is_dir to True."
            )
        elif filesuffix_set:
            # If a suffix is present, assume it's a file
            is_dir = False
            logger.debug("Suffix found. Assuming file. Setting is_dir to False.")
        else:
            # If the method cannot determine whether the path is for a file or directory, raise an error
            raise ValueError(
                "Failed to resolve if the path is a directory or a file. Ensure correct path and file_type are provided."
            )

        return is_dir

    def _check_existence(self, should_exist: bool):
        if should_exist and not self.path.exists():
            raise ValueError(
                f"The specified file or folder '{self.path}' does not exist, but existence is required."
            )

        elif not should_exist and self.path.exists():
            logger.warning(
                f"The specified file or folder '{self.path}' does exist, but existence is not required."
            )

    def _resolve_directory_type(self, file_type: str):
        """
        Handles the case when the specified path is a directory.
        """
        if self.path.is_file():
            raise ValueError(
                f"The specified path '{self.path}' is a file, not a directory."
            )
        # Create directory if it doesn't exist
        self.path.mkdir(exist_ok=True)
        resolved_file_type = FileType.from_suffix(file_type, raise_err=True)
        assert resolved_file_type.is_true_filetype()
        suffix = resolved_file_type.get_suffix()
        return resolved_file_type, suffix

    def _resolve_file_type(self, file_type: str, read_content: bool, add_suffix: bool):
        """
        Resolves the file type based on given parameters.

        Args:
            file_type (FileType or str, optional): An explicit file type or extension.
            read_content (bool): Indicates if file content should be used to help resolve the file type.
            add_suffix (bool): Whether to append the resolved file type's suffix to the file path.
        """
        resolved_file_type = self.__resolve_filetype__(
            file_type, self.path, read_content
        )
        assert resolved_file_type.is_true_filetype()

        # Get the suffix corresponding to the resolved file type
        suffix = resolved_file_type.get_suffix()

        # Optionally add suffix to the file path
        if add_suffix:
            self.path = self.path.with_suffix(suffix)

        return resolved_file_type, suffix

    def __resolve_filetype__(
        self, file_type: str, file_path: Path, read_content: bool
    ) -> FileType:
        """
        Determines the file type, utilizing the provided type, file path, or content as needed.

        Args:
            file_type (FileType or str, optional): An explicit file type or extension.
            file_path (str): The path to the file, used if file_type is not provided.
            read_content (bool): Indicates if file content should be used to help resolve the file type.

        Returns:
            FileType: The resolved file type.
        """
        if not file_type:
            try:
                return FileType.from_path(
                    file_path, read_content=read_content, raise_err=True
                )
            except EmptySuffixError:
                raise ValueError("filepath suffix is emtpy but file_type not set")

        resolved_file_type = FileType.from_suffix(file_type, raise_err=True)

        file_type_from_path = FileType.from_path(
            file_path, read_content=read_content, raise_err=False
        )

        if file_type_from_path.is_true_filetype():
            assert file_type_from_path == resolved_file_type

        return resolved_file_type

    def __str__(self):
        """
        Returns the absolute file path as a string.

        Returns:
            str: The resolved file path.
        """
        return str(Path(self.path).resolve())

    def __repr__(self):
        """
        Returns the absolute file path as a string.

        Returns:
            str: The resolved file path.
        """
        return f"{self.__class__.__name__}: {self.path.name}"


class InvalidOutputFormatError(Exception):
    """Exception raised when the output content format check fails after conversion."""

    def __init__(self, solving_tips):
        self.solving_tips = solving_tips
        super().__init__(
            "Output content format check failed after conversion and before writing. See solving tips for help."
        )

    def __str__(self):
        return f"{super().__str__()}\n\n### Some solving tips\n{self.solving_tips}\n"


class BaseConverter(ABC):
    """
    Abstract base class for file conversion, defining the template for input to output file conversion.
    """

    file_reader: FileReader = None
    file_writer: FileWriter = None
    folder_as_output: bool = None

    def __init__(
        self,
        input_files: Union[ResolvedInputFile, List[ResolvedInputFile]],
        output_file: ResolvedInputFile,
    ):
        """
        Sets up the converter with specified input and output files, ensuring compatibility.

        Args:
            input_files (Union[ResolvedInputFile, List[ResolvedInputFile]]): Either a single input file or a list of input files with resolved types.
            output_file (ResolvedInputFile): The output file where the converted data will be saved.
        """
        if isinstance(input_files, ResolvedInputFile):
            self.input_files = [input_files]
        elif isinstance(input_files, list):
            self.input_files = input_files
        else:
            raise TypeError(
                "input_files must be either a ResolvedInputFile or a list of ResolvedInputFile objects"
            )

        self.output_file = output_file
        self._check_file_types()

        # self.input_format = self.file_reader.input_format
        # self.output_format = self.file_writer.output_format
        self.check_io_handlers()

    def convert(self):
        """
        Orchestrates the file conversion process, including reading, converting, and writing the file.
        """
        logger.info("Starting conversion process...")

        # log
        logger.debug(
            f"Converting {self.input_files[0].path.name} and {len(self.input_files)-1} more ({self.get_supported_input_type()}) to {self.output_file.path.name} ({self.get_supported_output_type()})..."
        )
        logger.debug(f"Input files ({len(self.input_files)}): {self.input_files}")

        # Read all input files
        logger.info("Reading input file...")
        self._input_contents = [
            self._read_content(input_file.path) for input_file in self.input_files
        ]

        # Check input content format for all files
        logger.info("Checking input content format...")
        for input_content, input_file in zip(self._input_contents, self.input_files):
            logger.debug(f"Checking input content format for {input_file.path.name}...")
            assert self._check_input_format(
                input_content
            ), f"Input content format check failed for {input_file.path.name}"
        logger.debug("Input content format check passed")

        kwargs, output_path = self._get_convertion_kwargs(self.output_file.path)

        # Convert input files to output content
        logger.info("Converting files...")
        if self.file_writer is None:
            logger.info("Writing output directly")
            self._convert(input_contents=self._input_contents, **kwargs)
            logger.debug("Conversion complete")
        else:
            logger.info("Using output content")
            self.output_content = self._convert(input_contents=self._input_contents)
            # Check output content format
            solving_tips = self.__get_bad_output_content_solving_tips__()
            if not self._check_output_format(self.output_content):
                raise InvalidOutputFormatError(solving_tips)
            logger.debug("Output content format check passed")
            # save file
            logger.info("Writing output file...")
            self._write_content(output_path, self.output_content)
            logger.debug("Write complete")

        assert (
            output_path.exists()
        ), f"Output file {output_path.name} not found after conversion"

        logger.info(f"Output file: {output_path.resolve()}")
        logger.info("Conversion process complete.")

    def _get_convertion_kwargs(self, output_path: Path):
        kwargs = {}
        if self.folder_as_output:
            assert (
                output_path.is_dir()
            ), f"output_path {output_path} is not a dir while a folder is required for this conversion"
            kwargs["output_folder"] = output_path
        else:
            if output_path.is_dir():
                suffix = self.get_supported_output_type().get_suffix()
                output_path = (output_path / "opencf-output").with_suffix(suffix)
            kwargs["output_file"] = output_path
        return kwargs, output_path

    def _check_file_types(self):
        """
        Validates that the provided files have acceptable and supported file types for conversion.
        """
        for input_file in self.input_files:
            if not isinstance(input_file, ResolvedInputFile):
                raise ValueError(
                    f"Invalid input file. Expected: {ResolvedInputFile}. Actual: {type(input_file)}"
                )
            if input_file.file_type != self.get_supported_input_type():
                raise ValueError(
                    f"Unsupported input file type. Expected: {self.get_supported_input_type()}, Actual: {input_file.file_type}"
                )

        if not isinstance(self.output_file, ResolvedInputFile):
            raise ValueError(
                f"Invalid output file. Expected: {ResolvedInputFile}. Actual: {type(self.output_file)}"
            )
        if self.output_file.file_type != self.get_supported_output_type():
            raise ValueError(
                f"Unsupported output file type. Expected: {self.get_supported_output_type()}, Actual: {self.output_file.file_type}"
            )

    def check_io_handlers(self):
        """
        Ensures that valid I/O handlers (file reader and writer) are set for the conversion.
        """
        if self.file_reader is None:
            self.file_reader = SamePathReader()

        if not isinstance(self.file_reader, FileReader):
            raise ValueError("Invalid file reader")

        if self.file_writer is None:
            if self.folder_as_output is None:
                raise ValueError(
                    f"the class attribute folder_as_output should be set for your converter {self.__class__.__name__}"
                )
            return

        if not isinstance(self.file_writer, FileWriter):
            raise ValueError("Invalid file writer")

        self.folder_as_output = False

    @classmethod
    def get_input_type(cls):
        return cls.get_supported_input_type()

    @classmethod
    def get_output_type(cls):
        return cls.get_supported_output_type()

    @classmethod
    def get_supported_input_type(cls) -> FileType:
        """
        Defines the supported input file type for this converter.

        Returns:
            FileType: The file type supported for input.
        """
        input_type = cls._get_supported_input_type()
        if not isinstance(input_type, FileType):
            raise ValueError("Invalid supported input file type")
        return input_type

    @classmethod
    def get_supported_output_type(cls) -> FileType:
        """
        Defines the supported output file type for this converter.

        Returns:
            FileType: The file type supported for output.
        """
        output_type = cls._get_supported_output_type()
        if not isinstance(output_type, FileType):
            raise ValueError("Invalid supported output file type")
        return output_type

    @classmethod
    @abstractmethod
    def _get_supported_input_type(cls) -> FileType:
        """
        Abstract method to define the supported input file type by the converter.

        Returns:
            FileType: The supported input file type.
        """
        pass

    @classmethod
    @abstractmethod
    def _get_supported_output_type(cls) -> FileType:
        """
        Abstract method to define the supported output file type by the converter.

        Returns:
            FileType: The supported output file type.
        """
        pass

    @abstractmethod
    def _convert(
        self,
        input_contents: List,
        output_file: Optional[Path] = None,
        output_folder: Optional[Path] = None,
    ):
        """
        Abstract method to be implemented by subclasses to perform the actual file conversion process.
        """
        logger.info("Conversion method not implemented")

    def __get_bad_output_content_solving_tips__(self) -> str:
        _solving_tips = (
            f"If you convertion method (`{self.__class__.__name__}._convert(self, input_content:List[])`) uses only one input, make sure you select the first element of input_contents list before procedding",
        )
        return "\n".join(f"{i+1}. {elt}" for i, elt in enumerate(_solving_tips))

    def _read_content(self, input_path: Path):
        return self.file_reader._read_content(input_path)

    def _check_input_format(self, input_content):
        return self.file_reader._check_input_format(input_content)

    def _check_output_format(self, output_content):
        return self.file_writer._check_output_format(output_content)

    def _write_content(self, output_path: Path, output_content):
        return self.file_writer._write_content(output_path, output_content)
