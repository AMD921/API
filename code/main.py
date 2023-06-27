from fastapi import FastAPI
from auth_routes import auth_router
from order_routes import order_router
from fastapi_jwt_auth import AuthJWT
from schemas import Settings
import inspect, re
from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi.openapi.utils import get_openapi

app=FastAPI()



#?in tikke az api kollan dozdi shode serfan beshe az localhost:8000/docs estefade kard
"""https://github.com/IndominusByte/fastapi-jwt-auth/issues/34"""
def custom_openapi():
    """
    Customizes the OpenAPI schema for the FastAPI application.

    This function generates a custom OpenAPI schema for the FastAPI application.
    It sets the title, version, and description of the API.
    It also adds a security scheme for Bearer authentication and applies it to routes that require or optionally accept JWT tokens.

    Returns:
    - dict: The customized OpenAPI schema.

    Note:
    The `app` variable refers to the FastAPI application instance that this function is being called from.
    """
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title = "Pashmak Delivery API",
        version = "1.0",
        description = "An API for a Pashmak Delivery Service",
        routes = app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "Bearer Auth": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Enter: **'Bearer &lt;JWT&gt;'**, where JWT is the access token"
        }
    }

    # Get all routes where jwt_optional() or jwt_required
    api_router = [route for route in app.routes if isinstance(route, APIRoute)]

    for route in api_router:
        path = getattr(route, "path")
        endpoint = getattr(route,"endpoint")
        methods = [method.lower() for method in getattr(route, "methods")]

        for method in methods:
            # access_token
            if (
                re.search("jwt_required", inspect.getsource(endpoint)) or
                re.search("fresh_jwt_required", inspect.getsource(endpoint)) or
                re.search("jwt_optional", inspect.getsource(endpoint))
            ):
                openapi_schema["paths"][path][method]["security"] = [
                    {
                        "Bearer Auth": []
                    }
                ]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

@AuthJWT.load_config
def get_config():
    """
    Function to load configuration settings for AuthJWT.

    This function is called by the `AuthJWT` extension to retrieve the configuration settings.
    It returns an instance of the `Settings` model which provides the necessary configuration values.

    Returns:
    - Settings: An instance of the `Settings` model containing the configuration settings for AuthJWT.
    """
    return Settings()

app.include_router(auth_router)
app.include_router(order_router)