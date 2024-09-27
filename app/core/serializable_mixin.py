import json
from dataclasses import asdict, is_dataclass, fields
from typing import TypeVar, Type, Dict, Any

ModelClass = TypeVar('ModelClass', bound='SerializerMixin')


class SerializableMixin:
    """
    Mixin for serializing and deserializing model instances to/from dictionaries and JSON.
    """

    def to_dict(self) -> Dict[str, Any]:
        """Converts the dataclass model to a dictionary."""
        if is_dataclass(self):
            return asdict(self)
        raise TypeError("Only dataclass-based models can be serialized to dict.")

    @classmethod
    def from_dict(cls: Type[ModelClass], data: Dict[str, Any]) -> ModelClass:
        """Instantiates the model from a dictionary."""
        field_names = {f.name for f in fields(cls)}
        filtered_data = {k: v for k, v in data.items() if k in field_names}
        return cls(**filtered_data)

    def to_json(self) -> str:
        """Converts the model instance to a JSON string."""
        return json.dumps(self.to_dict(), default=str)

    @classmethod
    def from_json(cls: Type[ModelClass], json_str: str) -> ModelClass:
        """Instantiates the model from a JSON string."""
        try:
            data = json.loads(json_str)
            return cls.from_dict(data)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON data: {str(e)}") from e
