import logging
from http import HTTPStatus

from flask import Blueprint, request

from ..dto.user_dto import UserRequest
from ..handlers.response_handler import ResponseHandler
from ..repository.user_repository import UserRepository
from ..services.user_service import UserService
from ..utils.logging_utils import log

user_bp = Blueprint('users', __name__, '/users')

user_repository = UserRepository()
user_service = UserService(user_repository=user_repository)


@log(level=logging.INFO, include_time=True)
@user_bp.route('/', methods=['GET'])
def get_all_users():
    users = user_service.get_all_users()
    return ResponseHandler.ok("OK", status=HTTPStatus.OK, response_obj=users)


@log(level=logging.INFO, include_time=True)
@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = user_service.get_user(user_id)
    return ResponseHandler.ok("OK", status=HTTPStatus.OK, response_obj=user)


@log(level=logging.INFO, include_time=True)
@user_bp.route('/', methods=['POST'])
def create_user():
    data = request.get_json()
    user = UserRequest(**data)
    user_out = user_service.create_user(user)
    return ResponseHandler.ok("CREATED", status=HTTPStatus.CREATED, response_obj=user_out)


@log(level=logging.INFO, include_time=True)
@user_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    success = user_service.delete_user(user_id)
    return ResponseHandler.ok("ACCEPTED", status=HTTPStatus.ACCEPTED, response_obj=success)
