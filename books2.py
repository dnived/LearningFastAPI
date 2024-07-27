from fastapi import FastAPI, Body, HTTPException, status, Path
from pydantic import BaseModel, Field

app = FastAPI()

class Book():
    id:int
    title:str
    description:str
    author:str
    rating:int
    publish_date:int

    #constructor
    def __init__(self, id, title, description, author, rating, publish_date):
        self.id = id 
        self.title = title
        self.description = description
        self.author = author
        self.rating = rating
        self.publish_date = publish_date

#object that we will use to validate the incoming book request and then we will convert it into Book and save it
class BookRequest(BaseModel):
    id:int = Field(description="Id is not needed on create", default=None)
    title:str = Field(min_length=3)
    description:str = Field(min_length=3, max_length=250)
    author:str = Field(min_length=3)
    rating:int = Field(gt=0, lt=6)
    publish_date:int = Field(gt=2000, lt=2025)
    #swagger configuration this will show example of post request 
    model_config = {
        "json_schema_extra":{
            "example":{
                "title":"Title one",
                "description":"Nice Book",
                "author":"author one",
                "rating":5,
                "publish_date":2015
            }
        }
    }
    


BOOKS = [
    Book(1, "Learn Fast API", description="Best Course on FastAPI", author="Roby", rating=5, publish_date=2024),
    Book(2, "Learn React", description="Excellent course on React", author="Codevolution", rating=5,publish_date=2024),
    Book(3, "Flask for beginners", description="Awesome course on Flask", author="Linkedin Learning", rating=4, publish_date=2024),
    Book(4, "React Redux", description="Understand Redux", author="Youtube", rating=3, publish_date=2024),
]


def find_book_id(new_book: Book):
    # if len(BOOKS) > 0:
    #     new_book.id = BOOKS[-1].id+1
    # else:
    #     new_book.id = 1

    new_book.id = 1 if len(BOOKS)==0 else BOOKS[-1].id+1
    return new_book

    

            


@app.get("/books", status_code=status.HTTP_200_OK)
def get_all_book():
    return BOOKS

#adding a book without validation
# @app.post("/books/create_book")
# def create_a_book(book_request=Body()):
#     BOOKS.append(book_request)
#     return {"message":"book added successfully!!"}
    


#adding a book with validation
@app.post("/books/create_book", status_code=status.HTTP_201_CREATED)
#semicolon after book_request in create_a_book_request signifies book_request object should be of type BookRequest object
def create_a_book(book_request:BookRequest):

    # print(type(book_request))  # => <books2.BookRequest>
    # passing book_request dictionary to class Book
    # ** operator pass the key-value  from BookRequest() into the constructor of class BOOk
    # Book() -> it will convert the book_request to the type of class Book
    new_book = Book(**book_request.model_dump())

    # print(type(new_book))  # => <books2.Book>
    BOOKS.append(find_book_id(new_book))
    return {"message":"book added successfully!!"}



@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
def update_a_book(book_request:BookRequest):
    for i in range(len(BOOKS)):
        if(BOOKS[i].id == book_request.id):
            BOOKS[i] = book_request
            return {"message":"book updated successfully!!"}
        
    raise HTTPException(status_code=400, detail="Item not found")



@app.delete("/books/delete_book/{book_id}", status_code=status.HTTP_200_OK)
def delete_a_book(book_id:int=Path(gt=0)):
    for i in range (len(BOOKS)):
        if(BOOKS[i].id == book_id):
            BOOKS[i].pop
            return {"message":"book deleted successfully"}
    raise HTTPException(status_code=400, detail="Id does not found")