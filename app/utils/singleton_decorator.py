"""singleton_decorator.py"""

from abc import ABCMeta
from typing import Type, TypeVar, Callable, Any, cast

T = TypeVar('T', bound=Type[Any])


class SingletonABCMeta(ABCMeta):
    """
    A metaclass to implement the singleton pattern for abstract base classes.
    Ensures that only one instance of a class is created.
    """
    _instances: dict[Type[Any], Any] = {}

    def __call__(cls: T, *args: Any, **kwargs: Any) -> T:
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cast(T, cls._instances[cls])


class _SingletonWrapper:
    """
    A singleton wrapper class. Its instances would be created
    for each decorated class.
    """

    def __init__(self, cls: Type[T]) -> None:
        self.__wrapped__ = cls
        self._instance: T | None = None

    def __call__(self, *args: Any, **kwargs: Any) -> T:
        """Returns a single instance of decorated class"""
        if self._instance is None:
            self._instance = self.__wrapped__(*args, **kwargs)
        return cast(T, self._instance)


def singleton(cls: Type[T]) -> Callable[..., T]:
    """
    A singleton decorator. Returns a wrapper object. A call on that object
    returns a single instance object of decorated class. Use the __wrapped__
    attribute to access the decorated class directly in unit tests.
    """
    return _SingletonWrapper(cls)
