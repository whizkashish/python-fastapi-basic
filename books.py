from fastapi import Body, FastAPI

BOOKS = [
    {'title': 'title1', 'author': 'author1', 'category': 'science'},
    {'title': 'title2', 'author': 'author2', 'category': 'history'},
    {'title': 'title3', 'author': 'author', 'category': 'science'},
    {'title': 'title4', 'author': 'author4', 'category': 'science'},
    {'title': 'title5', 'author': 'author', 'category': 'fiction'},
    {'title': 'title6', 'author': 'author6', 'category': 'horror'},
]
app = FastAPI()
@app.get("/books")
async def read_all_books():
    return BOOKS

@app.get("/books/{book_title}")
async def read_All_books(book_title: str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book

@app.get("/books/")        
async def read_category_by_query(category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
        
    return books_to_return

@app.get("/books/byauthor/")        
async def books_by_author(author: str):
    print(author)
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == author.casefold():
            books_to_return.append(book)
        
    return books_to_return
        
@app.get("/books/{book_author}/")
async def read_author_category_by_query(book_author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == book_author.casefold() and\
            book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
        
    return books_to_return



@app.post("/books/create_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)


@app.put("/books/update_book")
async def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == updated_book['title'].casefold():
            BOOKS[i] = updated_book


@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
                BOOKS.pop(i)
                break


