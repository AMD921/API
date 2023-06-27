from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from database import Session, engine #!ep4 min 07:04
from schemas import SignUpModel, LoginModel
from models import User # 09:29
from fastapi.exceptions import HTTPException
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder


auth_router=APIRouter(
    prefix='/auth',
    tags=['auth']

)
"""
API router for handling authentication-related routes.

The `auth_router` is an instance of `APIRouter` that groups the authentication routes under the '/auth' prefix.
It is used to define and organize the authentication endpoints.
"""

session=Session(bind=engine)
"""
Create a database session using the SQLAlchemy session factory.

The `Session` object represents a database session and is created by calling the session factory (`Session`) with the database engine (`engine`) as the binding.
The session is used for interacting with the database, such as querying and modifying data.
"""

@auth_router.get('/')
async def hello(Authorize:AuthJWT=Depends()):
    """
    Sample route that requires authentication.

    This route requires a valid JWT access token for authorization.
    If the access token is valid, it returns a JSON response with a 'message' key set to 'Hello World'.
    If the access token is missing or invalid, it raises an HTTPException with a status code 401 (Unauthorized).

    Parameters:
    - Authorize (AuthJWT): The AuthJWT instance used for handling JWT authorization.

    Returns:
    - dict: A JSON response containing a 'message' key set to 'Hello World'.

    Raises:
    - HTTPException: If the access token is missing or invalid.
    """
    try:
        Authorize.jwt_required() #! 5: min 21:00

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"                    
        )

    return {"message":"Hello World"}


@auth_router.post('/signup',
    status_code=status.HTTP_201_CREATED
)
async def signup(user:SignUpModel):
    """
    Route for user signup.

    This route creates a new user based on the provided signup data.
    It performs validation checks to ensure that the username and email are unique.
    If the validation passes, it creates a new user record in the database.
    If the validation fails, it raises an HTTPException with a status code 400 (Bad Request).

    Parameters:
    - user (SignUpModel): The signup data submitted by the user.

    Returns:
    - User: The created user object.

    Raises:
    - HTTPException: If the username or email already exists.
    """
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

#login route

@auth_router.post('/login')
async def login(user:LoginModel,Authorize:AuthJWT=Depends()):
    """
    Route for user login.

    This route handles user authentication by validating the provided username and password.
    If the credentials are valid, it generates JWT access and refresh tokens and returns them in a JSON response.
    If the credentials are invalid, it raises an HTTPException with a status code 400 (Bad Request).

    Parameters:
    - user (LoginModel): The login credentials submitted by the user.
    - Authorize (AuthJWT): The AuthJWT instance used for handling JWT authorization.

    Returns:
    - dict: A JSON response containing the access and refresh tokens.

    Raises:
    - HTTPException: If the username or password is invalid.
    """

    db_user=session.query(User).filter(User.username==user.username).first()

    if db_user and check_password_hash(db_user.password, user.password):
        access_token=Authorize.create_access_token(subject=db_user.username)
        refresh_token=Authorize.create_refresh_token(subject=db_user.username)

        response={
            "access":access_token,
            "refresh":refresh_token
        }

        return jsonable_encoder(response)
    
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        detail="invalid Username or Password"
    )


#refresh tokens

@auth_router.get('/refresh')
async def refresh_token(Authorize:AuthJWT=Depends()):
    """
    Route for refreshing access tokens.

    This route handles refreshing access tokens by validating the provided refresh token.
    If the refresh token is valid, it generates a new access token and returns it in a JSON response.
    If the refresh token is invalid, it raises an HTTPException with a status code 401 (Unauthorized).

    Parameters:
    - Authorize (AuthJWT): The AuthJWT instance used for handling JWT authorization.

    Returns:
    - dict: A JSON response containing the new access token.

    Raises:
    - HTTPException: If the refresh token is invalid.
    """
    try:
        Authorize.jwt_refresh_token_required()

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Please provide a valid refresh token"
        )
    
    current_user=Authorize.get_jwt_subject()
    
    access_token=Authorize.create_access_token(subject=current_user)

    return jsonable_encoder({"access": access_token})