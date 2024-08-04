from fastapi import APIRouter, status, Depends, Path, HTTPException, Query
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from models import ToDos
from pydantic import BaseModel, Field
from .auth import get_current_user


#create the db
router = APIRouter()



#get the db session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#db dependency
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

#ToDo request Model to validate the incoming request
class ToDoRequest(BaseModel):
    title:str = Field(min_length=3, max_length=20)
    description:str = Field(min_length=3, max_length=200)
    priority:int = Field(gt=0, lt=6)
    complete:bool

    model_config={
        "json_schema_extra":{
            "example":{
                "title":"Todo Title",
                "description":"Todo Description",
                "priority":3,
                "complete":False
            }
        }
    }

#Get all ToDo
@router.get("/todos", status_code=status.HTTP_200_OK)
def get_all_todos(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    return db.query(ToDos).filter(ToDos.owner_id == user.get('id')).all()




#Get ToDo by Id
@router.get("/todos/{todo_id}", status_code=status.HTTP_200_OK)
def get_todo_by_id(user:user_dependency, db:db_dependency, todo_id:int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    todo_data = db.query(ToDos).filter(ToDos.id == todo_id).filter(ToDos.owner_id == user.get('id')).first()
    if todo_data is None:
        raise HTTPException(status_code=400, detail="Id doesn't exists")
    return todo_data



#Add a ToDo
@router.post("/todos/add_todo", status_code=status.HTTP_201_CREATED)
def add_todo(user: user_dependency, db:db_dependency, todo_request:ToDoRequest):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    todo_model = ToDos(**todo_request.model_dump(), owner_id=user.get('id'))
    db.add(todo_model)
    db.commit()



#Update a ToDo
@router.put("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_a_todo(user:user_dependency, db:db_dependency, todo_request:ToDoRequest, todo_id:int=Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    todo_model = db.query(ToDos).filter(ToDos.id == todo_id).filter(ToDos.owner_id==user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=400, detail="Id doesn't exists")
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()



#Delete a ToDo
@router.delete("/todos")
def delete_a_todo(user:user_dependency, db: db_dependency, todo_id:int = Query(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    todo_model = db.query(ToDos).filter(ToDos.id == todo_id).filter(ToDos.owner_id==user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=400, detail="Id doesn't exists")
    db.query(ToDos).filter(ToDos.id == todo_id).filter(ToDos.owner_id==user.get('id')).delete()
    db.commit()

