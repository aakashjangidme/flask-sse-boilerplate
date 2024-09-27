from dataclasses import dataclass
from datetime import datetime

from app.core.base_model import BaseModel


@dataclass
class UserModel(BaseModel):
    id: str
    username: str
    email: str
    is_active: str
    created_at: datetime
