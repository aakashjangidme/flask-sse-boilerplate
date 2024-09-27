from dataclasses import dataclass, field
from datetime import datetime

from app.core.base_dto import BaseDTO
from app.core.validator_mixin import required_validator, min_length_validator
from app.utils.class_helpers import validate


@dataclass
class UserResponse(BaseDTO):
    id: int = field(default_factory=int)
    username: str = field(default_factory=str)
    email: str = field(default_factory=str)
    is_active: bool = field(default_factory=bool)
    created_at: datetime = field(default_factory=datetime)


@validate
@dataclass
class UserRequest(BaseDTO):
    username: str = field(default_factory=str, metadata={'validators': [required_validator, min_length_validator(3)]})
    email: str = field(default_factory=str, metadata={'validators': [required_validator]})
