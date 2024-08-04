from fastapi import APIRouter, status, Depends, Path, HTTPException, Query
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from models import ToDos
from pydantic import BaseModel, Field
from .auth import get_current_user


#create the db
router = APIRouter(
        prefix="/admin",
    tags=["admin"]
)



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



@router.get('/todo', status_code=status.HTTP_200_OK)
def read_all(user:user_dependency, db:db_dependency):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail="Authentication Failed")
    return db.query(ToDos).all()