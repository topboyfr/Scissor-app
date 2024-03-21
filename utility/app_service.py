from typing import Generator
from database import database
from typing_extensions import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session

class functions:
    
    @staticmethod
    def get_db() -> Generator:
        try:
            db = database.SessionLocal()
            yield db
        finally:
            db.close()

db_session = Annotated[Session, Depends(functions.get_db)]


