from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#database url
SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"

#database engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread":False})

# database session => session allows us to configure the parameter for the session it will produce, such as the data engine, autoflush, autocommit and other options
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


#base (it is database object that we will use to interact with the database)
Base = declarative_base()