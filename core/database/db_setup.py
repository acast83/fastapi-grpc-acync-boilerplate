import os
from typing import Dict, Any

from tortoise import Tortoise

from core.configuration.configuration import load_configuration
from .db_credentials import DbCredentials

current_file_folder = os.path.dirname(os.path.realpath(__file__))


async def init_tortoise_for_services() -> None:
    """
    Asynchronously initializes Tortoise ORM for each service defined in the configuration.
    This function reads the service configurations and sets up Tortoise ORM connections and
    models for each service. It can optionally set up a separate test configuration.

    :return: None
    """
    config = load_configuration()
    db_credentials = DbCredentials()
    test_mode = os.getenv("test_mode", None)

    db_config: Dict[str, Dict[str, Any]] = {
        'connections': {},
        'apps': {},
    }
    models = []

    services = config.get("services", [])

    for service_name, service_config in services["grpc"].items():
        db_name = f'{db_credentials.application}_{service_name}'
        if not test_mode:
            db_url = f'postgres://{db_credentials.db_username}:{db_credentials.db_password}@{db_credentials.db_host}:{db_credentials.db_port}/{db_name}'
        else:
            db_url = f'postgres://{db_credentials.db_username}:{db_credentials.db_password}@{db_credentials.db_host}:{db_credentials.db_port}/test_{db_credentials.application}'
        db_config["connections"][service_name] = db_url
        models_path = f"services.grpc.{service_name}.models"
        db_config["apps"][service_name] = {
            'models': [models_path],
            'default_connection': service_name,
        }
        models.append(models_path)

    await Tortoise.init(config=db_config, modules={"models": models})
    await Tortoise.generate_schemas()


async def close_connections() -> None:
    """
    Closes all database connections established by Tortoise.

    This function should be called to clean up when the Tortoise ORM is no longer needed,
    typically at the end of the lifecycle of the application or after tests are run.

    :return: No return value (NoReturn)
    """
    await Tortoise.close_connections()
