from sqlmodel import Session, select
from typing import List
from .models import GlucoseTracker

def create_glucose_reading(session: Session, glucose_reading: GlucoseTracker):
    session.add(glucose_reading)
    session.commit()
    session.refresh(glucose_reading)
    return glucose_reading

def get_glucose_reading(session: Session, reading_id: int):
    return session.get(GlucoseTracker, reading_id)

def get_user_glucose_readings(session: Session, user_id: int, skip: int = 0, limit: int = 100):
    statement = select(GlucoseTracker).where(GlucoseTracker.user_id == user_id).offset(skip).limit(limit)
    return session.exec(statement).all()

def update_glucose_reading(
    session: Session,
    db_reading: GlucoseTracker,
    reading_update: dict
):
    for key, value in reading_update.items():
        setattr(db_reading, key, value)
    session.add(db_reading)
    session.commit()
    session.refresh(db_reading)
    return db_reading

def delete_glucose_reading(session: Session, db_reading: GlucoseTracker):
    session.delete(db_reading)
    session.commit()
    return {"ok": True}
