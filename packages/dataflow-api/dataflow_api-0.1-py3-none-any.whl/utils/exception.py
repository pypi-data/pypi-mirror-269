"""Custom exceptions for the project."""

from fastapi import HTTPException
from utils.logger import CustomLogger

# Initialize the logger
logger = CustomLogger().get_logger()


class CustomException(Exception):
    """
    Base class for custom exceptions.
    """

    def __init__(self, message):
        """
        Initialize the CustomException instance.

        Args:
            message (str): The error message associated with the exception.
        """
        super().__init__(message)

    def log_error(self):
        """
        Log the error message.
        """
        logger.error(str(self))



class DatabaseConnectionError(CustomException):
    """
    Exception for database connection errors.
    """

    def __init__(self, message):
        """
        Initialize the DatabaseConnectionError instance.

        Args:
            message (str): The error message associated with the exception.
        """
        super().__init__(message)
        logger.error(message)



class CompileError(HTTPException):
    """
    Exception for compile errors during requirements compilation.
    """

    def __init__(self, error_message: str):
        """
        Initialize the CompileError instance.

        Args:
            error_message (str): The error message associated with the compilation error.
        """
        super().__init__(status_code=500, detail=error_message)
        logger.error(error_message)



class FileNotFoundError(HTTPException):
    """
    Exception for file not found errors.
    """

    def __init__(self):
        """
        Initialize the FileNotFoundError instance.
        """
        error_message = "Error: requirements.in file not found"
        super().__init__(status_code=500, detail=error_message)
        logger.error(error_message)



class ResolutionImpossibleError(HTTPException):
    """
    Exception for resolution impossible errors during dependency resolution.
    """

    def __init__(self):
        """
        Initialize the ResolutionImpossibleError instance.
        """
        error_message = "Error: ResolutionImpossible - Dependency resolution impossible"
        super().__init__(status_code=500, detail=error_message)
        logger.error(error_message)



class DistributionNotFoundError(HTTPException):
    """
    Exception for distribution not found errors.
    """

    def __init__(self):
        """
        Initialize the DistributionNotFoundError instance.
        """
        error_message = "Error: DistributionNotFound - Distribution not found"
        super().__init__(status_code=500, detail=error_message)
        logger.error(error_message)



class InstallationError(HTTPException):
    """
    Exception for errors during package installation.
    """

    def __init__(self):
        """
        Initialize the InstallationError instance.
        """
        error_message = "Error: InstallationError - Error during package installation"
        super().__init__(status_code=500, detail=error_message)
        logger.error(error_message)



class OtherCompileError(HTTPException):
    """
    Exception for other compile errors.
    """

    def __init__(self):
        """
        Initialize the OtherCompileError instance.
        """
        error_message = "Error compiling requirements"
        super().__init__(status_code=500, detail=error_message)
        logger.error(error_message)



class InternalServerError(HTTPException):
    """
    Exception for internal server errors.
    """

    def __init__(self):
        """
        Initialize the InternalServerError instance.
        """
        error_message = "Internal Server Error"
        super().__init__(status_code=500, detail=error_message)
        logger.error(error_message)
