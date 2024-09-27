import logging
from contextlib import contextmanager
from sqlite3 import Connection, Cursor, Row, connect, PARSE_DECLTYPES
from typing import Tuple, List, Union, Any, Dict

from app.database.database_client import DatabaseClient
from app.utils.singleton_decorator import singleton

logger = logging.getLogger(__name__)


@singleton
class SQLiteClient(DatabaseClient):
    def __init__(self, connection_str: str, timeout: int = 5) -> None:
        super().__init__(connection_str)
        self.timeout: int = timeout
        self.connection: Connection | None = None

    def connect(self) -> None:
        """Establish a connection to the SQLite database."""
        self.connection = connect(
            self.connection_str,
            timeout=self.timeout,
            detect_types=PARSE_DECLTYPES
        )
        self.connection.row_factory = Row
        logger.debug("Connected to SQLiteClient")

    def close(self) -> None:
        """Close the connection to the SQLite database."""
        if self.connection:
            self.connection.close()
            logger.debug("Closed SQLiteClient connection")
            self.connection = None

    @contextmanager
    def _get_cursor(self) -> Cursor:
        """Context manager for acquiring and releasing a database cursor."""
        if not self.connection:
            raise RuntimeError("No connection established.")
        cursor = self.connection.cursor()
        try:
            yield cursor
        finally:
            cursor.close()

    def execute(self, query: str, params: Tuple[Any, ...] = ()) -> None:
        """Execute a query with optional parameters."""
        try:
            with self._get_cursor() as cursor:
                cursor.execute(query, params)
                self.connection.commit()
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            raise

    def fetch_all(self, query: str, params: Tuple[Any, ...] = ()) -> List[Dict[str, Any]]:
        """Fetch all rows from a query."""
        try:
            with self._get_cursor() as cursor:
                cursor.execute(query, params)
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error fetching all rows: {e}")
            raise

    def fetch_one(self, query: str, params: Tuple[Any, ...] = ()) -> Union[Dict[str, Any], None]:
        """Fetch one row from a query."""
        try:
            with self._get_cursor() as cursor:
                cursor.execute(query, params)
                row = cursor.fetchone()
                if row:
                    return dict(row)
                return None
        except Exception as e:
            logger.error(f"Error fetching one row: {e}")
            raise
