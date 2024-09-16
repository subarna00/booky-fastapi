from fastapi import APIRouter,status, Depends
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List

from src.db.main import get_session
from .schemas import UserModel, UserCreateModel
from .service import UserService

user_service = UserService()
auth_router = APIRouter()

@auth_router.post('/signup',status_code=status.HTTP_201_CREATED)
async def create_user_account(user: UserCreateModel,session: AsyncSession = Depends(get_session)):
    # return user
    email = user.email
    user_exists = await user_service.user_exists(email,session)
    if user_exists:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User with email already exists")
    
    new_user = await user_service.create_user(user,session)
    return new_user