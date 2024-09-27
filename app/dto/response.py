from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime
from http import HTTPStatus
from typing import Any

from app.core.base_dto import BaseDTO


@dataclass
class Response(BaseDTO, ABC):
    timestamp: datetime = field(default_factory=datetime.now)
    status: int = HTTPStatus.OK
    message: str | None = None
    data: Any = None


@dataclass
class ErrorResponse(Response):
    details: str | None = None
