from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import datetime
from sqlmodel import select, desc

from  .schemas import BookCreateModel,BookUpdateModel
from .models import Books


class BookService:

    async def get_all_books(self,session: AsyncSession):
        statement = select(Books).order_by(desc(Books.created_at))
        result = await session.exec(statement)
        return result.all()


    async def get_book(self,book_uid: str, session: AsyncSession):
        statement = select(Books).where(Books.uid == book_uid)
        result = await session.exec(statement)
        book = result.first()

        return book if book is not None else None


    async def create_book(self, book_data: BookCreateModel,session: AsyncSession):
        book_data_dict = book_data.model_dump()
        new_book = Books(**book_data_dict)
        # new_book.published_date = datetime.strptime(book_data_dict["published_date"],'%Y-%m-%d')
        session.add(new_book)
        await session.commit()
        return new_book


    async def update_book(self, book_uid:str, book_data:BookUpdateModel ,session: AsyncSession):
        book_to_update = await self.get_book(book_uid,session)

        if book_to_update is not None:

            update_data_dict = book_data.model_dump()
            
            for k,v in update_data_dict.items():
                setattr(book_to_update,k,v)
            
            await session.commit()
            return book_to_update
        else:
            return None


    async def delete_book(self,book_uid:str,session: AsyncSession):
        book_to_delete = await self.get_book(book_uid,session)

        if book_to_delete is not None:
            await session.delete(book_to_delete)
            await session.commit()
            return {}
        else:
            return None