"""
MIME Type Guesser Module

This module provides a singleton class for guessing MIME types from file paths using the python-magic library.
"""

try:
    import magic  # pip install python-magic
except ImportError:
    magic = None


class MimeGuesser:
    """
    Singleton class for guessing MIME types from file paths using the python-magic library.
    """

    _instance = None

    def __new__(cls):
        """
        Creates a new instance of the class if it doesn't exist already.

        Returns:
            MimeGuesser: The instance of the MimeGuesser class.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.mime_guesser = None

            # Initialize the mime_guesser if magic module is available
            if magic is not None:
                cls._instance.mime_guesser = magic.Magic(mime=True)

        return cls._instance

    def get_mime_guesser(self):
        """
        Returns the mime_guesser instance.

        Returns:
            magic.Magic: The instance of the mime_guesser.
        """
        return self.mime_guesser

    @classmethod
    def guess_mime_type_from_file(cls, file_path):
        """
        Guesses the MIME type from the file path.

        Args:
            file_path (str): The path to the file.

        Returns:
            str: The guessed MIME type.

        Raises:
            ImportError: If the python-magic library is not imported.
        """
        if not cls._instance.mime_guesser:
            raise ImportError(
                "magic module is not imported. Please install it with 'pip install python-magic'"
            )

        return cls._instance.mime_guesser.from_file(file_path)


def guess_mime_type_from_file(file_path):
    """
    Guesses the MIME type from the file path.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The guessed MIME type.
    """
    return MimeGuesser().guess_mime_type_from_file(str(file_path))
