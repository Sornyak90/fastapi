from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel

app = FastAPI()

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)

books = [
    {
        "id": 1,
        "title": "Book 1",
        "authors": "Author 1",
    },
    {
        "id": 2,
        "title": "Book 2",
        "authors": "Author 2",
    },

]

@app.get(
    "/books", 
    tags=["Книги"],
    summary="Получить все книги", 
    
)
def root():
    return books

@app.get(
    "/books/{book_id}",
    tags=["Книги"],
    summary="Получить книгу",
    
)
def get_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book
    raise   HTTPException(status_code=404, detail="Book not found")

class NewBook(BaseModel):
    title: str
    authors: str


@app.post(
    "/books",
    tags=["Книги"],
    summary="Добавление новой книги",
)
def create_book(new_book: NewBook):
    books.append({
        "id": len(books) + 1,
        **new_book.dict(),
    })
    return {"success": True, "massage": "Book created successfully"}
    




    
     

