from sqlmodel import Session, SQLModel, create_engine
from typing import Annotated
from fastapi import Depends
import os

LOGIN = os.environ.get('PS_LOGIN')
PASS = os.environ.get('PS_PASS')
PORT = os.environ.get('PS_PORT')

engine = create_engine(f"postgresql://{LOGIN}:{PASS}@127.0.0.1:{PORT}/POS")


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
        
SessionDep = Annotated[Session, Depends(get_session)]
