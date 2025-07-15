from fastapi import Depends
from sqlmodel import Session
from core.database import get_session

def get_db():
    return Depends(get_session)
