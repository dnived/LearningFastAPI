from fastapi import FastAPI, Body

app = FastAPI()


books_data = [
    {"title": "title One", "author":"author one", "category":"science"},
    {"title": "title Two", "author":"author Two", "category":"science"},
    {"title": "title Three", "author":"author Three", "category":"science"},
    {"title": "title Four", "author":"author Four", "category":"math"},
    {"title": "title Five", "author":"author Five", "category":"math"},
]

# @app.get("/")
# def first_route():
#     return "Hello from FastAPI"



@app.get("/book/mybook")
def read_all_book():
    return books_data

# #path parameter
# @app.get("/book/{book_title}")
# def read_book_by_title(book_title:str):
#     for book in books_data:
#         if(book.get("title").casefold()== book_title.casefold()):
#             return book
        


#path parameter v2
@app.get("/book/{book_title}")
def read_book_by_title(book_title):
    for book in books_data:
        print(book.get("title"), book.get("title").casefold(), book_title.casefold())
        if(book.get("title").casefold() == book_title.casefold()):
            return book



#Query parameter
@app.get("/books/")
def read_book_by_query(book_category:str):
    books_to_return = []
    for book in books_data:
        if(book.get("category").casefold() == book_category.casefold()):
            books_to_return.append(book)
    return books_to_return




#Path and Query parameter
@app.get("/books/{book_author}/")
def read_book_path_category(book_category:str, book_author:str):
    books_to_return=[]
    for book in books_data:
        if(book.get("author").casefold() == book_author and book.get("category") == book_category.casefold()):
            books_to_return.append(book)
    return books_to_return


#Post route
@app.post("/books/create_book")
def create_a_book(new_request=Body()):
    books_data.append(new_request)
    return {"message":"Book added successfully!!"}


#Put Request
@app.put("/books/update_book")
def update_a_book(update_book=Body()):
    print(update_book)
    for i in range(len(books_data)):
        if(books_data[i].get("title").casefold() ==  update_book.get("title").casefold()):
            books_data[i] = update_book
    return {"message":"book updated successfully!!"}


@app.delete("/books/delete_book/{book_title}")
def delete_a_book(book_title:str):
    for i in range(len(books_data)):
        if(books_data[i].get("title").casefold() == book_title.casefold()):
            books_data[i].pop
            break
    return {"message":"book deleted successfully!!"}
