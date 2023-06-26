from fastapi import APIRouter, status
from database import Session, engine #!ep4 min 07:04
from schemas import SignUpModel
from models import User # 09:29
from fastapi.exceptions import HTTPException
from werkzeug.security import generate_password_hash, check_password_hash

auth_router=APIRouter(
    prefix='/auth',
    tags=['auth']

)


session=Session(bind=engine)

@auth_router.get('/')
async def hello():
    return {"message":"Hello World"}


@auth_router.post('/signup',
    status_code=status.HTTP_201_CREATED
)
async def signup(user:SignUpModel):
    db_email=session.query(User).filter(User.email == user.email).first()

    if db_email is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with the email already exists"
                             
        ) #400 bad request
    db_username=session.query(User).filter(User.username == user.username).first()

    if db_username is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with the username already exists"
                             
        )

    new_user=User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),           #installed werkzeug here
        first_name=user.first_name,
        last_name=user.last_name,
        address=user.address,
        phone=user.phone,
        is_active=user.is_active,
        is_staff=user.is_staff,
    )

    session.add(new_user)

    session.commit()

    return new_user