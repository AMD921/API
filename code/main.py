from fastapi import FastAPI
from auth_routes import auth_router
from order_routes import order_router
from fastapi_jwt_auth import AuthJWT
from schemas import Settings
app=FastAPI()

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