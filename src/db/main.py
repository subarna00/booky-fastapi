from sqlmodel import create_engine, text, SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

from src.config import Config

engine = create_async_engine(
    url= Config.DATABASE_URL,
    echo=True
)


async def init_db():
    try:
        async with engine.begin() as conn:
            from src.books.models import Book
            await conn.run_sync(SQLModel.metadata.create_all)
            print("Database initialized successfully")
    except Exception as e:
        print(f"Error during database initialization: {e}")


async def get_session()-> AsyncSession:
    Sesion = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with Sesion() as session:
        yield session