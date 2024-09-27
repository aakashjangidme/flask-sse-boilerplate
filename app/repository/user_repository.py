import logging

from app.core.base_repository import BaseRepository
from ..database.database_client import DatabaseClient
from ..database.db import pg_db
from ..dto.user_dto import UserRequest
from ..models.user_model import UserModel
from ..utils.logging_utils import log
from ..utils.singleton_decorator import singleton

logger = logging.getLogger(__name__)


@singleton
class UserRepository(BaseRepository):
    class Meta:
        __model__ = UserModel

    def __init__(self, db_client: DatabaseClient = None):
        self.db: DatabaseClient = pg_db if db_client is None else db_client

    @log(include_time=True)
    def get_all_users(self) -> list[UserModel]:
        query = "SELECT id, username, email, is_active, created_at FROM users"
        try:
            result = self.db.fetch_all(query)
            return self.map_to_model(result, model_cls=self.Meta.__model__, many=True)
        except Exception as e:
            logger.error(f"Error fetching all users: {e}")
            raise

    @log(include_time=True)
    def get_user_by_id(self, user_id: int) -> UserModel | None:
        query = "SELECT id, username, email, is_active, created_at FROM users WHERE id = %s"
        try:
            result = self.db.fetch_one(query, (user_id,))
            return self.map_to_model(result, model_cls=self.Meta.__model__) if result else None
        except Exception as e:
            logger.error(f"Error fetching user by ID {user_id}: {e}")
            raise

    @log(include_time=True)
    def create_user(self, new_user: UserRequest) -> UserModel | None:
        username, email = new_user
        query = "INSERT INTO users (username, email, is_active) VALUES (%s, %s, %s)  RETURNING id"
        try:
            self.db.execute(query, (username, email, True))

            get_user_q = "SELECT id, username, email, is_active, created_at FROM users WHERE username = %s AND email = %s"

            new_user = self.db.fetch_one(get_user_q, (username, email))

            if not new_user:
                raise ValueError(f"Could not retrieve user ID after insertion for {username=}, {email=}")

            return self.map_to_model(new_user, model_cls=self.Meta.__model__) if new_user else None
        except Exception as e:
            logger.error(f"Error creating user {username}: {e}")
            raise

    @log(include_time=True)
    def delete_user(self, user_id: int) -> bool:
        query = "DELETE FROM users WHERE id = %s"
        try:
            self.db.execute(query, (user_id,))
            self.db.connection.commit()
            return True
        except Exception as e:
            logger.error(f"Error deleting user with ID {user_id}: {e}")
            self.db.connection.rollback()

            raise
