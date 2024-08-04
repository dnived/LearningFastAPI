from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel, Field
from models import Users
# from passlib.context import CryptContext
import bcrypt
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm  import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
# from jose import jwt
import jwt
from dotenv import load_dotenv
import os
from datetime import timedelta, datetime, timezone


#Load constants
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


#router
router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


#bcrypt context 
# bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


class CreateUserRequest(BaseModel):
    username:str 
    email:str
    first_name:str
    last_name:str
    password:str
    role:str

class Token(BaseModel):
    access_token:str
    token_type:str

#get the db session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#db dependency
db_dependency = Annotated[Session, Depends(get_db)]

def authenticate_user(username, password, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    # if not bcrypt_context.verify(password, user.hashed_Password):
    if not bcrypt.checkpw(password.encode('utf-8'), user.hashed_Password):
        return False
    return user

def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role: str = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='could not validate user')
        return {'username':username, 'id':user_id, 'user_role':user_role}
    except jwt.JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='could not validate user')


def create_access_token(username :str, user_id:int, role:str, expires_delta: timedelta):
    # encode = {'sub':username, 'id':user_id}
    # expires = datetime.now(timezone.utc) + expires_delta
    # encode.update({'exp':expires})
    encode={
        'sub':username,
        'id': user_id,
        'role':role,
        'exp': datetime.now(timezone.utc) + expires_delta
    }
    return jwt.encode(encode, SECRET_KEY, ALGORITHM)




#create user
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(db:db_dependency, create_user:CreateUserRequest):
    create_user_model = Users(
        email = create_user.email,
        username = create_user.username,
        first_name = create_user.first_name,
        last_name = create_user.last_name,
        # hashed_Password = bcrypt_context.hash(create_user.password),
        hashed_Password = bcrypt.hashpw(create_user.password.encode('utf-8'), bcrypt.gensalt()),
        role = create_user.role,
        is_active = True
    )

    # password.encode('utf-8'): Converts the password string to a bytes object using UTF-8 encoding. This step is necessary because bcrypt.hashpw does not accept string types and requires bytes.
    db.add(create_user_model)
    db.commit()

#authenticate user
@router.post("/token", response_model=Token)
def login_access_token(form_data:Annotated[OAuth2PasswordRequestForm, Depends()], db:db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
       raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='could not validate user')
    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=20))
    return {'access_token':token, 'token_type':'Bearer'}























# import jwt
# from datetime import datetime, timedelta

# SECRET_KEY = "your_secret_key"
# ALGORITHM = "HS256"

# def create_access_token(username: str, user_id: int, expires_delta: timedelta):
#     encode = {'sub': username, 'id': user_id}
#     expires = datetime.utcnow() + expires_delta
#     encode.update({'exp': expires})
#     return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

# def decode_access_token(token: str):
#     try:
#         return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#     except jwt.ExpiredSignatureError:
#         print("Token has expired")
#     except jwt.InvalidTokenError:
#         print("Invalid token")
