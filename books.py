from fastapi import FastAPI, Body


app = FastAPI()


#book class
class Books():
    id:int
    title:str
    description:str
    author:str
    rating:str

    def __init__(self, id, title,description,author,rating):
        self.id = id
        self.title = title
        self.description = description
        self.author = author
        self.rating = rating

BOOKS = [
    Books(1, "Learn FastAPI", description="best FastAPI Course", author="Udemy", rating="5"),
    Books(2, "Learn React", description="Nice React Course", author="Youtube", rating="4"),
    Books(3, "Learn Redux", description="Awesome Redux Course", author="Youtube", rating="4"),
    Books(4, "Learn Mongo", description="Interesting mongo Course", author="Coursera", rating="5"),
]

@app.get("/books")
def get_all_book():
    return BOOKS


@app.get("/books/{book_title}")
def get_book_by_title(book_title:str):
    for book in BOOKS:
        if(book.get("title").casefold() == book_title.casefold()):
            return book
    
#adding a validation
@app.post("/books/create_book")
def create_a_book(book_request=Body()):
    BOOKS.append(book_request)
    return {"message":"book added successfully!!"}