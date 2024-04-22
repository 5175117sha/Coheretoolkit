import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from typing import Annotated, Generator, Any
from fastapi import Depends

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, pool_size=5, max_overflow=10, pool_timeout=30
)


def get_session() -> Generator[Session, Any, None]:
    with Session(engine) as session:
        yield session


DBSessionDep = Annotated[Session, Depends(get_session)]
