import logging
from contextlib import contextmanager
from typing import Tuple, List, Union, Any, Dict, Sequence

from psycopg import OperationalError, DatabaseError, Cursor
from psycopg.rows import RowFactory
from psycopg_pool import ConnectionPool

from app.database.database_client import DatabaseClient
from app.utils.logging_utils import log
from app.utils.singleton_decorator import singleton

logger = logging.getLogger(__name__)


class DictRowFactory(RowFactory[Any]):
    def __init__(self, cursor: Cursor[Any]) -> None:
        self.fields = [c.name for c in cursor.description] if cursor.description else []

    def __call__(self, values: Sequence[Any]) -> Dict[str, Any]:
        if len(self.fields) != len(values):
            raise ValueError("Mismatch between fields and values")
        if not self.fields:
            return {}
        return dict(zip(self.fields, values))


@singleton
class PostgresClient(DatabaseClient):
    def __init__(self, connection_str: str, timeout: int = 5, pool_size: int = 10) -> None:
        super().__init__(connection_str)
        self.timeout: int = timeout
        self.pool_size: int = pool_size
        self.pool: ConnectionPool | None = None

    def connect(self) -> None:
        """Initialize connection pool if not already initialized."""
        if self.pool is None:
            try:
                self.pool = ConnectionPool(
                    conninfo=self.connection_str,
                    min_size=self.pool_size,
                    timeout=self.timeout
                )
                logger.info("Successfully initialized PostgreSQL connection pool")
            except OperationalError as e:
                logger.error(f"Failed to initialize PostgreSQL connection pool: {e}")
                raise ConnectionError("Could not establish connection to PostgreSQL.") from e

    @contextmanager
    def _get_cursor(self, row_factory: RowFactory[Any] = DictRowFactory) -> Cursor[Any]:
        """Context manager for acquiring and releasing a database cursor."""
        self.connection = self.pool.getconn()
        try:
            yield self.connection.cursor(row_factory=row_factory)
        finally:
            self.pool.putconn(self.connection)

    def close(self) -> None:
        """Close the connection pool."""
        if self.pool:
            self.pool.close()
            logger.info("Closed all connections in the PostgreSQL pool")

    @log(include_time=True)
    def execute(self, query: str, params: Tuple[Any, ...] = ()) -> None:
        """Execute a query with optional parameters."""
        try:
            with self._get_cursor() as cursor:
                res = cursor.execute(query, params or ())
                logger.debug(f"inserted {res.rowcount} rows")
                cursor.connection.commit()
                return res.rowcount
        except DatabaseError as e:
            logger.error(f"Error executing query: {e}")
            cursor.connection.rollback()
            raise

    def fetch_all(self, query: str, params: Tuple[Any, ...] = ()) -> List[Dict[str, Any]]:
        """Fetch all rows from a query."""
        try:
            with self._get_cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
        except DatabaseError as e:
            logger.error(f"Error fetching all rows: {e}")
            raise

    def fetch_one(self, query: str, params: Tuple[Any, ...] = ()) -> Union[Dict[str, Any], None]:
        """Fetch one row from a query."""
        try:
            with self._get_cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchone()
        except DatabaseError as e:
            logger.error(f"Error fetching one row: {e}")
            raise
