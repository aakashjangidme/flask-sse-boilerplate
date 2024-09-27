import abc
from typing import TypeAlias

from app.core.base_dto import DTOClass
from app.utils.class_helpers import auto_repr

ResponseType: TypeAlias = DTOClass


class BaseService(metaclass=abc.ABCMeta):
    """
    Base class for services that provides a fluent interface for processing responses.
    """
    ...

    __repr__ = auto_repr
