from typing import Optional, Union, Any

from app.utils.class_helpers import auto_repr, auto_str


class APIException(Exception):
    """
    Base exception for all API-related errors.

    Attributes:
        code (int): HTTP status code.
        message (str): Error message.
        details (Optional[str]): Additional details about the error.
    """

    def __init__(self, code: int = 500, message: Optional[str] = None, details: Any = None):
        self.code = code
        self.message = message or self.get_default_message()
        self.details = details
        super().__init__(self.message)

    @staticmethod
    def get_default_message() -> str:
        """
        Provides a default message for the exception.
        """
        return "An unexpected error occurred."

    __repr__ = auto_repr
    __str__ = auto_str


class NotFoundException(APIException):
    """
    Exception for resource not found errors.

    Args:
        resource (str): Name of the resource that was not found.
        identifier (Union[str, int]): The identifier for the resource (e.g., ID or name).
    """

    def __init__(self, resource: Optional[str] = None, identifier: Optional[Union[str, int]] = None):
        message = f"{resource} with identifier '{identifier}' not found." if resource and identifier \
            else "Resource not found."
        super().__init__(code=404, message=message)


class UnauthorizedException(APIException):
    """
    Exception for unauthorized access.

    Args:
        action (Optional[str]): The action that was attempted.
    """

    def __init__(self, action: Optional[str] = None):
        message = f"Unauthorized to perform action: {action}." if action else "Unauthorized to perform this action."
        super().__init__(code=401, message=message)


class BadRequestException(APIException):
    """
    Exception for bad request errors.

    Args:
        message (Optional[str]): Description of the bad request error.
    """

    def __init__(self, message: Optional[str] = None, details=None):
        super().__init__(code=400, message=message or "Bad request.", details=details)


class ForbiddenException(APIException):
    """
    Exception for forbidden actions.

    Args:
        action (Optional[str]): The forbidden action.
    """

    def __init__(self, action: Optional[str] = None):
        message = f"Action '{action}' is forbidden." if action else "Action is forbidden."
        super().__init__(code=403, message=message)


class ConflictException(APIException):
    """
    Exception for conflicts, such as duplicate records.

    Args:
        resource (Optional[str]): The resource involved in the conflict.
    """

    def __init__(self, resource: Optional[str] = None):
        message = f"Conflict detected for resource: {resource}." if resource else "Conflict detected."
        super().__init__(code=409, message=message)


class BadValueError(BadRequestException):
    def __init__(self, message: Optional[str] = None, details=None):
        super().__init__(message=message or "Bad request.", details=details)
