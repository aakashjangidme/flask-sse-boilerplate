from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, Tuple, List, Union

from app.utils.class_helpers import auto_repr


class DatabaseType(Enum):
    POSTGRES = 'postgres'
    SQLITE = 'sqlite'
    ORACLE = 'oracle'


class DatabaseClient(ABC):
    def __init__(self, connection_str: str) -> None:
        self.connection_str = connection_str
        self.connection = None
        self.cursor = None

    @abstractmethod
    def connect(self) -> None:
        """Establish a connection to the database."""
        ...

    @abstractmethod
    def close(self) -> None:
        """Close the connection to the database."""
        pass

    @abstractmethod
    def execute(self, query: str, params: Tuple[Any, ...] = ()) -> Any:
        """Execute a query with optional parameters."""
        pass

    @abstractmethod
    def fetch_all(self, query: str, params: Tuple[Any, ...] = ()) -> List[Dict[str, Any]]:
        """Fetch all rows from a query."""
        pass

    @abstractmethod
    def fetch_one(self, query: str, params: Tuple[Any, ...] = ()) -> Union[Dict[str, Any], None]:
        """Fetch one row from a query."""
        pass

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    __repr__ = auto_repr
