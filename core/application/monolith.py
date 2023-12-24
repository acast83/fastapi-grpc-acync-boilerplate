from importlib import import_module
from typing import Union, Any

from fastapi import FastAPI
from fastapi.routing import APIRoute, Mount
from starlette.routing import Route

from core.configuration.configuration import load_configuration


def get_monolith_app() -> FastAPI:
    """
    Initialize and return a FastAPI application by mounting apps defined in the configuration.

    This function reads the configuration which specifies the services to be included in the monolith.
    Each service with an `app` attribute is mounted onto the main FastAPI application.

    Returns:
        FastAPI: The main FastAPI application with all the service apps mounted.
    """
    # app = FastAPI()
    app = FastAPI(docs_url="/api/docs", redoc_url="/api/redocs", openapi_url="/api/openapi.json")

    config = load_configuration()

    services = config.get("services", [])
    assert services, "No services defined in configuration"
    for service in services["rest"]:
        try:
            service_module = import_module(f"services.rest.{service}.api")
        except Exception as e:
            raise
        service_app = getattr(service_module, "app", None)
        if service_app:
            app.mount(f"/api/{service.replace('_', '-')}", service_app, name=service)

    return app


def print_route_methods(route: Union[APIRoute, Route, Any]) -> None:
    """
    Prints out the methods and path for a given API route.
    Args:
        route (Union[APIRoute, Route, Any]): The route object from FastAPI or Starlette.
    """
    if isinstance(route, APIRoute):
        # Ensure that methods is not None
        assert route.methods is not None, "route.methods should not be None"
        methods = ', '.join(route.methods)
        print(f"API {methods}: {route.path} - Name: {route.name}")
    elif isinstance(route, Route):
        # Ensure that methods is not None
        assert route.methods is not None, "route.methods should not be None"
        methods = ', '.join(route.methods)
        print(f"DOCS {methods}: {route.path} - Name: {route.name}")
    else:
        print(f"OTHER: {route.path} - Name: {route.name}")


def list_all_routes(app: FastAPI, prefix: str = '') -> None:
    """
    Recursively lists all routes for a given FastAPI application, including those mounted on sub-applications.

    Args:
        app (FastAPI): The FastAPI application or sub-application to list routes from.
        prefix (str, optional): The URL path prefix for the routes. Defaults to an empty string.
    """
    for route in app.routes:
        if isinstance(route, (APIRoute, Route)):
            print_route_methods(route)
        elif isinstance(route, Mount):
            assert isinstance(route.app, FastAPI)
            list_all_routes(route.app, prefix=prefix + route.path)


monolith_app = get_monolith_app()

__all__ = ["monolith_app", "list_all_routes"]
