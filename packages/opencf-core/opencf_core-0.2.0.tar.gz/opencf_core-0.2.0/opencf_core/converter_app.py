"""
Main Module

This module contains the main application logic.
"""

from pathlib import Path
from typing import Dict, List, Optional, Tuple, Type

from .base_converter import BaseConverter, ResolvedInputFile
from .filetypes import FileType
from .logger import logger


class BaseConverterApp:
    """
    Main application class responsible for managing file conversions.
    """

    converters: List[Type[BaseConverter]] = []

    def __init__(
        self,
        input_file_paths: List[str],
        input_file_type: Optional[str] = None,
        output_file_path: Optional[str] = None,
        output_file_type: Optional[str] = None,
    ):
        """
        Initializes the BaseConverterApp instance.

        Args:
            input_file_paths (List[str]): List of paths to the input files.
            input_file_type (FileType, optional): The type of the input file. Defaults to None.
            output_file_path (str, optional): The path to the output file. Defaults to None.
            output_file_type (FileType, optional): The type of the output file. Defaults to None.
        """
        self._dict_converters: Dict[Tuple[FileType, FileType], Type[BaseConverter]] = {}

        if not isinstance(input_file_paths, list):
            raise TypeError("input_file_paths sould be a list")
        if len(input_file_paths) == 0:
            raise ValueError("input_file_paths should not be a empty list")

        self.input_files = [
            ResolvedInputFile(
                input_file_path,
                is_dir=False,
                should_exist=True,
                file_type=input_file_type,
                add_suffix=False,
                read_content=True,
            )
            for input_file_path in input_file_paths
        ]

        self.input_file_type = self.input_files[0].file_type
        assert self.input_file_type.is_true_filetype()

        if not output_file_path:
            output_file_path = str(Path(input_file_paths[0]).with_suffix(""))
            add_suffix_to_output_path = True
            assert (
                output_file_type is not None
            ), "either output_file_path or output_file_type should be set "
        else:
            add_suffix_to_output_path = False

        self.output_file = ResolvedInputFile(
            output_file_path,
            is_dir=None,
            should_exist=False,
            file_type=output_file_type,
            add_suffix=add_suffix_to_output_path,
            read_content=False,
        )
        self.output_file_type = self.output_file.file_type

        for _conv_class in self.converters:
            self.add_converter_pair(_conv_class)

    def add_converter_pair(self, converter_class: Type[BaseConverter]):
        """
        Adds a converter pair to the application.

        Args:
            converter_class (Type[BaseConverter]): The converter class to add.

        Raises:
            ValueError: If the converter class is invalid.
        """
        # Check if the converter_class is a subclass of BaseConverter
        if not issubclass(converter_class, BaseConverter):
            raise ValueError("Invalid converter class")

        # Add the converter pair to the converters dictionary
        self._dict_converters[
            (converter_class.get_input_type(), converter_class.get_output_type())
        ] = converter_class

    def get_supported_conversions(self) -> Tuple[Tuple[FileType, FileType], ...]:
        """
        Retrieves the supported conversions.

        Returns:
            Tuple[Tuple[FileType, FileType]]: A tuple of tuples representing supported conversions.
        """
        return tuple(self._dict_converters.keys())

    def run(self):
        """
        Runs the conversion process.
        """
        # get converter class
        converter_class = self._dict_converters.get(
            (self.input_file_type, self.output_file_type)
        )

        # make sure a converter class exists
        if converter_class is None:
            _ = "\n " + "\n ".join(
                map(lambda x: f"* {x[0]} -> {x[1]}", self.get_supported_conversions())
            )
            logger.error(
                f"Conversion from {self.input_file_type} to {self.output_file_type} not supported. Supported convertions are : {_}"
            )
            return

        # instanciate the converter
        converter = converter_class(self.input_files, self.output_file)

        # run the convertion pipeline
        converter.convert()
