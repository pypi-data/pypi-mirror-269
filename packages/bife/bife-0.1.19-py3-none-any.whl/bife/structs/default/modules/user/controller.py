from fastapi import APIRouter, Depends, HTTPException, Response, status
from libs.security.security import Security

from .events import UserEvents
from .ext import (
    InvalidEmail,
    InvalidGender,
    InvalidName,
    InvalidPassword,
    InvalidUserLogin,
    InvalidUsername,
    UserAlreadyExists,
    UserNotFound,
)
from .models import UserModel
from .repository import UserRepository
from .schemas import LoginUserRequest, RegisterUserRequest, UserAuthResponse
from .service import UserService

router: APIRouter = APIRouter(tags=['user'], prefix='/user')
security: Security = Security()

repository: UserRepository = UserRepository()
service: UserService = UserService()
events: UserEvents = UserEvents()


@router.post('/login', response_model=UserAuthResponse)
def user_login(data: LoginUserRequest, response: Response):
    try:
        user = repository.login_user(data)
    except UserNotFound as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, e.args[0])
    except (InvalidPassword, InvalidUserLogin) as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, e.args[0])

    tokens = service.generate_access_token(user.uuid)
    response.set_cookie('access_token', tokens['access_token'])
    response.set_cookie('refresh_access_token', tokens['refresh_access_token'])
    return UserAuthResponse(**tokens)


@router.post('/register', response_model=UserAuthResponse)
def register_user(data: RegisterUserRequest, response: Response):
    try:
        user = repository.register_user(data)
    except (
        InvalidUsername,
        InvalidEmail,
        InvalidGender,
        InvalidName,
        InvalidPassword,
    ) as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, e.args[0])
    except UserAlreadyExists as e:
        raise HTTPException(status.HTTP_409_CONFLICT, e.args[0])
    tokens = service.generate_access_token(user.uuid)
    response.set_cookie('access_token', tokens['access_token'])
    response.set_cookie('refresh_access_token', tokens['refresh_access_token'])
    return UserAuthResponse(**tokens)


@router.get('/me')
def get_about_user(
    current_user: UserModel = Depends(security.get_current_user),
):
    return current_user.__dict__
