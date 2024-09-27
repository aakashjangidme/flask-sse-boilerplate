from app.core.base_service import BaseService
from app.dto.user_dto import UserResponse, UserRequest
from app.exceptions.api_exception import NotFoundException
from app.repository.user_repository import UserRepository
from app.utils.logging_utils import log
from app.utils.singleton_decorator import singleton


@singleton
class UserService(BaseService):

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    @log()
    def get_all_users(self) -> list[UserResponse]:
        users = self.user_repository.get_all_users()
        response = UserResponse.from_model(users, many=True)
        return response

    @log()
    def get_user(self, user_id) -> UserResponse | None:
        user = self.user_repository.get_user_by_id(user_id)

        if not user:
            raise NotFoundException(resource="User", identifier=user_id)

        response = UserResponse.from_model(user, many=False)
        return response

    @log()
    def create_user(self, new_user: UserRequest) -> UserResponse:
        user = self.user_repository.create_user(new_user)
        return UserResponse.from_model(user)

    @log()
    def delete_user(self, user_id) -> bool:
        return self.user_repository.delete_user(user_id)
