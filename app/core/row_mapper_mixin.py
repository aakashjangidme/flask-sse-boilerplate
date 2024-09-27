from dataclasses import fields
from typing import TypeVar, Type, Dict, Any, Tuple, List

RowType = Dict[str, Any] | Tuple[Any, ...]
ModelClass = TypeVar('ModelClass', bound='RowMapperMixin')


class RowMapperMixin:
    """
    Mixin for converting model instances from database rows (tuples/dictionaries).
    """

    @classmethod
    def _from_row(cls: Type[ModelClass], row: RowType) -> ModelClass:
        """Create a model instance from a dictionary or tuple."""
        if isinstance(row, dict):
            return cls(**row)
        elif isinstance(row, tuple):
            if len(row) != len(fields(cls)):
                raise ValueError("Tuple length does not match the number of model fields.")
            return cls(*row)
        raise TypeError("Unexpected type for row data.")

    @classmethod
    def from_row(cls: Type[ModelClass], row: RowType, many: bool = False) -> ModelClass | List[ModelClass]:
        """Create a model instance or a list of model instances from row data."""
        if many:
            if isinstance(row, list):
                return [cls._from_row(r) for r in row]
            raise ValueError("Expected a list of rows.")
        return cls._from_row(row)
