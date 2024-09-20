from fastapi import APIRouter,status, Depends
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.responses import JSONResponse
from datetime import timedelta

from src.db.main import get_session
from .schemas import UserModel, UserCreateModel,UserLoginModel
from .service import UserService
from .utils import create_access_token,decode_token,verify_password

user_service = UserService()
auth_router = APIRouter()

REFRESH_TOKEN_EXPIRY =2

@auth_router.post('/signup',status_code=status.HTTP_201_CREATED)
async def create_user_account(user: UserCreateModel,session: AsyncSession = Depends(get_session)):
    # return user
    email = user.email
    user_exists = await user_service.user_exists(email,session)
    if user_exists:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User with email already exists")
    
    new_user = await user_service.create_user(user,session)
    return new_user

@auth_router.post('/login')
async def login_users(login_data: UserLoginModel,session: AsyncSession = Depends(get_session)):
    email = login_data.email
    password = login_data.password

    user = await user_service.get_user_by_email(email,session)

    if user is not None:
        password_valid = verify_password(password,user.password)
        if password_valid:
            access_token = create_access_token(
                user_data={
                    'email':user.email,
                    'user_uid': str(user.uid)
                }
                )
            
            refresh_token = create_access_token(
                user_data={
                    'email':user.email,
                    'user_uid': str(user.uid)
                },
                refresh=True,
                expiry= timedelta(days=REFRESH_TOKEN_EXPIRY)
            )

            return JSONResponse(
                content={
                    "message":"Login Successfull",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user":{
                        "email": user.email,
                        "uid": str(user.uid)
                    }
                }
            )

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Invalid Email or Password"
    )       