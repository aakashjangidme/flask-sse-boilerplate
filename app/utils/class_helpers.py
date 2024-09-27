"""class_helpers.py"""


def auto_repr(self) -> str:
    """Return a detailed string representation for debugging purposes."""
    class_name = self.__class__.__name__
    attributes = ', '.join(f"{key}={repr(value)}" for key, value in self.__dict__.items())
    return f"{class_name}({attributes})"


def auto_str(self) -> str:
    """Return a concise string representation for user-friendly display."""
    class_name = self.__class__.__name__
    attributes = ', '.join(f"{key}={value}" for key, value in self.__dict__.items())
    return f"{class_name}({attributes})"


def validate(cls):
    """
    Decorator to mark a dataclass as requiring validation.
    """
    cls._validate = True
    return cls
