"""logging_utils.py"""

import functools
import logging
import time
from typing import Callable

import colorlog
# Define a LogFilter to add request_id to log records
from flask import g, has_request_context, request


# Request Filter to include request context details in logs
class RequestFilter(logging.Filter):
    def filter(self, record):
        if has_request_context():
            record.url = request.url or "-"
            record.remote_addr = request.remote_addr or "-"
            record.request_id = getattr(g, "request_id", "-") or "-"
        else:
            record.url = "-"
            record.remote_addr = "-"
            record.request_id = "-"
        record.app_code = getattr(record, "app_code", "application-X") or "-"
        return True


def setup_logging():
    handler = colorlog.StreamHandler()
    formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s [%(levelname)s] [%(request_id)s] [%(filename)s:%(lineno)d] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        },
        style='%'
    )
    handler.setFormatter(formatter)

    logger = logging.getLogger()

    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    logger.addFilter(RequestFilter())
    handler.addFilter(RequestFilter())


def log(level: int = logging.DEBUG, include_time: bool = False, suppress_exceptions: bool = False) -> Callable:
    """
    Decorator to log function calls, arguments, and optionally measure execution time with color output.

    Args:
        level (int): Logging level (default: logging.DEBUG).
        include_time (bool): Whether to log the execution time of the function (default: False).
        suppress_exceptions (bool): If True, exceptions will be logged but not raised (default: False).

    Returns:
        Callable: Decorated function with logging.
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            # Handle the case for methods within classes
            if hasattr(func, '__self__'):
                qualname = f"{func.__self__.__class__.__name__}.{func.__name__}"

            else:
                qualname = func.__name__

            logger = logging.getLogger(qualname)

            start_time = time.time() if include_time else None

            # Create a readable signature of function arguments
            args_repr = [repr(a) for a in args]
            kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
            signature = ", ".join(args_repr + kwargs_repr)

            # Log function call
            logger.log(level, f"Called {qualname}({signature})")

            try:
                # Execute the function
                result = func(*args, **kwargs)

                # Log the result
                logger.log(level, f"{qualname} returned {result!r}")

                # Log execution time if enabled
                if include_time:
                    duration = (time.time() - start_time) * 1000
                    logger.log(level, f"{qualname} executed in {duration:.2f} milliseconds")

                return result
            except Exception as e:
                # Log exception
                logger.exception(f"Exception raised in {qualname} with args: {signature}")
                if suppress_exceptions:
                    return None
                raise e

        return wrapper

    return decorator
