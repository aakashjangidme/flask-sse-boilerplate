import logging

import werkzeug
from flask import request

from app.exceptions.api_exception import APIException
from app.handlers.response_handler import ResponseHandler

logger = logging.getLogger(__name__)


def init_app(app):
    @app.errorhandler(APIException)
    def handle_api_exception(ex: APIException):
        """
        Handles custom APIException.
        Logs the error and returns a formatted error response.
        """

        if ex.code == 500:
            logger.exception(ex)
        else:
            logger.error(ex, exc_info=False)

        return ResponseHandler.error(message=ex.message, status=ex.code, details=ex.details)

    @app.errorhandler(werkzeug.exceptions.HTTPException)
    def handle_http_exception(ex: werkzeug.exceptions.HTTPException):
        """
        Handles Werkzeug HTTP exceptions.
        Logs the error and returns a formatted error response.
        """
        if ex.code == 500:
            logger.exception(f"HTTPException 500: {ex}")
        else:
            logger.error(f"HTTPException {ex.code}: {ex}")

        # Extract the original exception message if available
        message = getattr(ex, "original_exception", str(ex))
        return ResponseHandler.error(message=str(message), status=ex.code, details=str(ex))

    @app.errorhandler(Exception)
    def handle_generic_exception(ex: Exception):
        """
        Handles all other exceptions.
        Logs the error and returns a formatted error response.
        """

        logger.exception(f"Unhandled Exception: {ex}")

        # Determine if the request is API-based and handle accordingly
        if request.path.startswith('/api/'):
            return ResponseHandler.error(message="An unexpected error occurred.", status=500, details=str(ex))

        # For non-API paths, you might want to return a generic error page or similar
        return ResponseHandler.error(message="An unexpected error occurred.", status=500, details=str(ex))
