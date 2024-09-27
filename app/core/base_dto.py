from dataclasses import dataclass
from typing import TypeVar, List, Union, Type

from app.core.base_model import BaseModel

DTOClass = TypeVar('DTOClass', bound='BaseDTO')


@dataclass
class BaseDTO(BaseModel):
    """Base Data Transfer Object class for handling model-to-DTO conversion and validation."""

    def __post_init__(self):
        self.run_validations()

    @classmethod
    def from_model(cls: Type[DTOClass], model: Union[BaseModel, List[BaseModel]], many: bool = False) \
            -> Union[DTOClass, List[DTOClass]]:
        """Create a DTO instance or a list of DTO instances from a model or a list of models."""
        if many:
            if isinstance(model, list):
                return [cls._from_model(m) for m in model]
            else:
                raise ValueError("Expected a list of models.")
        else:
            return cls._from_model(model)

    @classmethod
    def _from_model(cls: Type[DTOClass], model: BaseModel) -> DTOClass:
        """Convert a single model instance to a DTO instance."""
        return cls.from_dict(model.to_dict())
