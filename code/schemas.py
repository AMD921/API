"""this file is going to help us validate the different data that we're going to give to the api
it's also going to help us to return our responses from our api"""

from pydantic import BaseModel
from typing import Optional

class SignUpModel(BaseModel):
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
        orm_mode=True
        schema_extra={
            'example': {
                "username":"amd921",
                "email":"aminmohammad.davoudi@gmail.com",
                "password":"password",
                "first_name:":"Amin Mohammad",
                "last_name":"Davoudi",
                "address":"Chalous",
                "phone":'09197761148',
                "is_staff":False,
                "is_active":True
            }
        }


class Settings(BaseModel):
    authjwt_secret_key:str='f32d64c9d15fc3968fbade8525ff2d099d300f4a6ef6abdafcb96d50256d654e' #?import secrets; secrets.token_hex()


class LoginModel(BaseModel):
    username:str
    password:str


#6
class OrderModel(BaseModel):
    id:Optional[int]
    quantity:int
    order_status:Optional[str]="PENDING"
    bag_size:Optional[str]="SMALL"
    user_id:Optional[int]


    class Config:
        orm_mode=True
        schema_extra={
            "example":{
                "quantity":2,
                "bag_size":"LARGE"
            }
        }