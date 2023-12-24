import asyncio
import logging
import os
import pathlib
from functools import wraps
from typing import Callable, Type, Any

from fastapi import HTTPException, status

from core.configuration.configuration import load_configuration


def setup_logging() -> None:
    """
    Set up logging for each service defined in the configuration.
    It reads the logging level from the environment variable LOGGING_LEVEL
    and sets up file and stream handlers for each service's logger.
    """
    logging_level = os.environ.get('LOGGING_LEVEL', 'INFO').upper()
    numeric_level = getattr(logging, logging_level, None)
    if not isinstance(numeric_level, int):
        raise ValueError(f'Invalid log level: {logging_level}')

    logs_folder = str(pathlib.Path(__file__).parent.parent.parent / "logs")
    if not os.path.exists(logs_folder):
        # If the directory does not exist, create it
        os.makedirs(logs_folder)

    for service in load_configuration()["services"]["grpc"].keys():
        initiate_logging_for_service(service, numeric_level)

    for service in load_configuration()["services"]["rest"].keys():
        initiate_logging_for_service(service, numeric_level)


def initiate_logging_for_service(service: str, numeric_level: int) -> None:
    logger = logging.getLogger(service)
    logger.setLevel(numeric_level)

    log_file_path = pathlib.Path(__file__).parent.parent.parent / "logs" / f"{service}.log"
    if not os.path.exists(log_file_path):
        # If the file does not exist, create it
        with open(str(log_file_path), 'w') as file:
            file.write('')  # Writing an e

    file_handler = logging.FileHandler(log_file_path)
    formatter = logging.Formatter("%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s",
                                  "%Y-%m-%d %H:%M:%S")
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)


def exception_traceback_logging(logger: logging.Logger) -> Callable:
    """
    Decorator for logging exceptions in asynchronous functions.

    Args:
        logger (logging.Logger): The logger to use for logging exceptions.

    Returns:
        Callable: A decorator that can be applied to asynchronous functions.
    """

    def decorator(funct: Callable) -> Callable:
        @wraps(funct)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return await funct(*args, **kwargs)
            except HTTPException as http_exc:
                # Re-raise the original HTTPException
                raise http_exc
            except Exception as e:
                # Log the exception and raise a 500 Internal Server Error
                logger.exception(f"An exception occurred in {funct.__name__}: {e}")
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return wrapper

    return decorator


def class_exception_traceback_logging(logger: logging.Logger) -> Callable:
    """
    Class decorator for applying exception_traceback_logging to all async methods of a class.

    Args:
        logger (logging.Logger): The logger to use for logging exceptions.

    Returns:
        Callable: A class decorator.
    """

    def class_decorator(cls: Type) -> Type:
        for name, method in cls.__dict__.items():
            if callable(method) and asyncio.iscoroutinefunction(method):
                setattr(cls, name, exception_traceback_logging(logger)(method))
        return cls

    return class_decorator


def get_test_logger() -> logging.Logger:
    """
    Creates and returns a test logger configured with basic settings.

    Returns:
        logging.Logger: The configured logger.
    """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    return logging.getLogger('test_logger')


if __name__ == "__main__":
    setup_logging()
