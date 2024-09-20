
from fastapi import APIRouter,status, Depends
from fastapi.exceptions import HTTPException
from typing import List
from sqlmodel.ext.asyncio.session import AsyncSession

from src.books.schemas import Book,BookUpdateModel,BookCreateModel
from src.db.main import get_session
from src.books.service import BookService
from src.auth.dependencies import AccessTokenBearer

book_router = APIRouter()
book_service = BookService()
access_token_bearer = AccessTokenBearer()

@book_router.get('/',response_model=List[Book])
async def get_all_books(session:AsyncSession = Depends(get_session),user_details=Depends(access_token_bearer) ):
    books = await book_service.get_all_books(session)
    return books


@book_router.post("/",status_code=status.HTTP_201_CREATED, response_model=Book)
async def create_a_book(book_data: BookCreateModel,session:AsyncSession = Depends(get_session) )-> dict:
    new_book = await book_service.create_book(book_data,session)
    return new_book


@book_router.get("/{book_uid}",status_code=status.HTTP_200_OK,response_model=Book)
async def get_book(book_uid: str,session:AsyncSession = Depends(get_session)) -> dict:
    book = await book_service.get_book(book_uid,session)

    if book:
        return book
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@book_router.patch("/{book_uid}",response_model=Book)
async def update_book(book_uid: str,booki: BookUpdateModel,session:AsyncSession = Depends(get_session)) -> dict:
    updated_book = await book_service.update_book(book_uid,booki,session)

    if updated_book is not None:
        return updated_book
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@book_router.delete("/{book_uid}")
async def delete_book(book_uid: str,session:AsyncSession = Depends(get_session)) -> dict:
    book_to_delete = await book_service.delete_book(book_uid,session)

    if book_to_delete is not None:
        return {}
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
