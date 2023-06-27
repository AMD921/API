"""this file is going to help us validate the different data that we're going to give to the api
it's also going to help us to return our responses from our api"""

from pydantic import BaseModel
"""
Import the `BaseModel` class from the `pydantic` module.

`BaseModel` is a base class provided by Pydantic for creating data models with validation and serialization capabilities.
"""

from typing import Optional
"""
Import the `Optional` type hint from the `typing` module.

`Optional` is used to indicate that a variable can have either a specified type or be `None`.
"""


class SignUpModel(BaseModel):
    """
    Data model for user sign-up information.
    """

    id:Optional[int]
    username:str
    email:str
    password:str
    first_name:Optional[str]
    last_name:Optional[str]
    address:Optional[str]
    phone:Optional[str]
    is_staff:Optional[bool]
    is_active:Optional[bool]
    """after this we're going to configure our model to work with our orm (sqlalchemy)"""

    class Config:
        """
        Configuration class for the `SignUpModel` data model.
        """

        orm_mode=True
        schema_extra={
            'example': {
                "username":"amd921",
                "email":"aminmohammad.davoudi@gmail.com",
                "password":"password",
                "first_name:":"Amin Mohammad",
                "last_name":"Davoudi",
                "address":"Chalous",
                "phone":"09197761148",
                "is_staff":False,
                "is_active":True
            }
        }


class Settings(BaseModel):
    """
    Data model for application settings.

    Attributes:
    - authjwt_secret_key (str): The secret key used for authentication and JWT token encryption.

        The `authjwt_secret_key` attribute is a string that represents the secret key used for authentication and JWT token encryption.
        It is recommended to generate a secure secret key and replace the default value with the generated key.
        One way to generate a secure secret key is by using the `secrets` module in Python and its `token_hex()` function.
        To generate a secure secret key, uncomment the import statement for the `secrets` module and the line starting with `secrets.token_hex()`,
        then assign the generated value to `authjwt_secret_key`.

        Example:
        ```
        import secrets
        ...

        class Settings(BaseModel):
            authjwt_secret_key: str = secrets.token_hex()
        ```

        Note: Keep the secret key confidential and do not hardcode sensitive information in your source code.
        It is recommended to store the secret key securely, such as using environment variables or a configuration file.
    """
    authjwt_secret_key:str='f32d64c9d15fc3968fbade8525ff2d099d300f4a6ef6abdafcb96d50256d654e' #?import secrets; secrets.token_hex()


class LoginModel(BaseModel):
    """
    Data model for user login information.
    """

    username:str
    password:str


#6
class OrderModel(BaseModel):
    """
    Data model for an order.
    """

    id:Optional[int]
    quantity:int
    order_status:Optional[str]="PENDING"
    bag_size:Optional[str]="SMALL"
    user_id:Optional[int]


    class Config:
        """
        Configuration class for the `OrderModel` data model.
        """

        orm_mode=True
        schema_extra={
            "example":{
                "quantity":2,
                "bag_size":"LARGE"
            }
        }


#12
class OrderStatusModel(BaseModel):
    """
    Data model for order status.
    """

    order_status:Optional[str]="PENDING"

    class Config:
        """
        Configuration class for the `OrderStatusModel` data model.
        """

        orm_mode = True
        schema_extra={
            "example":{
                "order_status":"PENDING"
            }
        }