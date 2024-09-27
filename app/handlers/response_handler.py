from http import HTTPStatus

from flask import jsonify

from app.dto.response import Response, ErrorResponse
from app.utils.dttm_utils import DateUtils


class ResponseHandler:
    @staticmethod
    def ok(message: str, status: int, response_obj: object) -> tuple:
        """
        Generate a JSON response with a status code.

        Args:
            message (str): A message to include in the response.
            status (int): The HTTP status code for the response.
            response_obj (dict|BaseModel): The data to include in the response.

        Returns:
            tuple: A tuple containing the JSON response and the status code.
        """
        # Create a Response instance
        response = Response(
            message=message,
            status=status,
            data=response_obj,
            timestamp=DateUtils.get_dttm_local(serialized=True)
        )

        return jsonify(response.to_dict()), status

    @staticmethod
    def error(message: str, status: int = HTTPStatus.INTERNAL_SERVER_ERROR, response_obj: object = None,
              details=None) -> tuple:
        """
        Generate a JSON response with a status code.

        Args:
            message (str): A message to include in the response.
            status (int): The HTTP status code for the response.
            response_obj (dict|BaseModel): The data to include in the response.

        Returns:
            tuple: A tuple containing the JSON response and the status code.
            :param response_obj:
            :param message:
            :param status:
            :param details:
        """

        response = ErrorResponse(
            message=message,
            status=status,
            data=response_obj,
            timestamp=DateUtils.get_dttm_local(serialized=True), details=details
        )

        return jsonify(response.to_dict()), status
