from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status
from typing import Optional
app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date
        

class BookRequest(BaseModel):
    id: Optional[int] = Field("Field is optional")
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str =  Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gt=1999, lt=2031)

    class Config:
        json_schema_extra = {
            'example': {
                'title': 'A new Book',
                'author': 'Codewithimmi',
                'description': 'A new description of a book',
                'rating': 5,
                'published_date':2022
            }
        }



BOOKS = [
    Book(1, 'Computer Scince Pro', 'codingwithimmi', 'A very nice Book', 5, 2021),
    Book(2, 'Be fast with fast api', 'codingwithimmi', 'A very nice Book', 5, 2022),
    Book(3, 'Master endpoint', 'codingwithimmi', 'A Awsome Book', 5, 2023),
    Book(4, 'HP1', 'Author 1', 'A very nice Book', 5, 2024),
    Book(5, 'HP2', 'Author 2', 'A very nice Book', 5, 2022),
    Book(6, 'HP3', 'Author 3', 'A very nice Book', 5, 2021),
]

@app.get("/books", status_code=status.HTTP_200_OK)
def read_all_books():
    return BOOKS


@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    
    raise HTTPException(status_code=404, detail="Item not Found")

@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating: int = Query(gt=0,lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)

    return books_to_return

@app.get("/books/published_date/", status_code=status.HTTP_200_OK)
async def read_book_by_published_date(published_date: int= Query(gt=1999, lt=2031)):
    books_to_return = []
    for book in BOOKS:
        if book.published_date == published_date:
            books_to_return.append(book)

    return books_to_return

@app.post("/createbook", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))

def find_book_id(book: Book):

    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book

@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed = True
            break

    if not book_changed:
        raise HTTPException(status_code=404, detail="Item not Found")
        

@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
            break

    if not book_changed:
        raise HTTPException(status_code=404, detail="Item not Found")