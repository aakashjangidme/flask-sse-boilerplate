from dataclasses import dataclass, astuple

from app.core.row_mapper_mixin import RowMapperMixin
from app.core.serializable_mixin import SerializableMixin
from app.core.validator_mixin import ModelValidatorMixin


@dataclass
class BaseModel(SerializableMixin, RowMapperMixin, ModelValidatorMixin):
    """Base Model class providing common functionalities for model classes."""

    def __iter__(self):
        return iter(astuple(self))
