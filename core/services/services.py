import os
import re
from fastapi import HTTPException, status, Request

from core.configuration.configuration import load_configuration


def get_service_name(request: Request) -> str:
    # Provide a default value for the port if the environment variable is not set
    monolith_app_port = os.getenv("MONOLITH_APP_PORT", "8080")

    # Ensure that the default_port_value is a string that represents a valid integer
    if request.scope["server"][-1] in (int(monolith_app_port), None):
        path_url = request.url.path
        service_name = path_url.split('/')[2]
        return service_name
    port = request.scope["server"][-1]

    config = load_configuration()

    # Loop through the services in the configuration
    for service_name, service_config in config["services"].items():
        # Check if the port number matches the service's port number
        if service_config["port"] == port:
            return service_name

    raise HTTPException(status.HTTP_404_NOT_FOUND, detail="SERVICE_NOT_FOUND")


def extract_service_name(url) -> str | None:
    match = re.search(r'/api-gateway/([^/]+)', url)
    if match:
        return match.group(1)
    return None
