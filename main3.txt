from typing import Annotated

from fastapi import FastAPI, Depends
from pydantic import BaseModel

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column 

app = FastAPI()

engine = create_async_engine("sqlite+aiosqlite:///books.db")

new_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_session():
    async with new_session() as session:
        yield session

SessionDep = Annotated[AsyncSession,Depends(get_session)]

class Base(DeclarativeBase):
    pass

class BookModel(Base):
    __tablename__ = "books"
    id : Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    authors: Mapped[str]

@app.post("/setup_database")
async def setup_datebase():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {"ok":True, "massage": "Database setup successfully"}

class BoookAddSchema(BaseModel):
    title: str
    authors: str

class BoookSchema(BoookAddSchema):
    id: int


@app.post("/books")
async def add_book(data: BoookAddSchema, session: SessionDep):
    new_book = BookModel(
        title =data.title,
        authors=data.authors,
    )
    session.add(new_book)
    await session.commit()
    return {"ok":True, "massage": "Add successfully"}
    

@app.get("/books")
async def get_books(session: SessionDep):
    query = select(BookModel)
    result = await session.execute(query)
    return result.saclars().all()    
    