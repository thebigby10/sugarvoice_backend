from fastapi import APIRouter, Depends, HTTPException, Body
from sqlmodel import Session
from typing import List, Optional
from datetime import datetime

from auth_service.models import User
from auth_service.auth import get_current_user
from core.database import get_session
from .models import GlucoseTracker, GlucoseTrackerCreate, GlucoseTrackerRead, GlucoseTrackerUpdate
from .crud import (
    create_glucose_reading,
    get_glucose_reading,
    get_user_glucose_readings,
    update_glucose_reading,
    delete_glucose_reading
)

router = APIRouter(
    tags=["glucose"]
)

@router.post("/glucose/", response_model=GlucoseTrackerRead)
def create_simple_reading(
    *,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    level: float = Body(...),
    time: Optional[datetime] = Body(default_factory=datetime.utcnow),
    before_after_bed: str = Body(...)
):
    """Create a new glucose reading with minimal inputs, automatically using the authenticated user"""
    if not current_user or not current_user.id:
        raise HTTPException(status_code=401, detail="Authentication required")

    glucose_data = {
        "level": level,
        "time": time,
        "before_after_bed": before_after_bed,
        "user_id": current_user.id
    }

    db_reading = GlucoseTracker(**glucose_data)
    return create_glucose_reading(session, db_reading)

@router.post("/", response_model=GlucoseTrackerRead)
def create_reading(
    *,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    glucose_reading: GlucoseTrackerCreate
):
    """Create a new glucose reading for the current user"""
    if not current_user or not current_user.id:
        raise HTTPException(status_code=401, detail="Authentication required")

    db_reading = GlucoseTracker(**glucose_reading.dict())
    db_reading.user_id = current_user.id
    return create_glucose_reading(session, db_reading)

@router.get("/", response_model=List[GlucoseTrackerRead])
def read_user_readings(
    *,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100
):
    """Get all glucose readings for the current user"""
    if not current_user or not current_user.id:
        raise HTTPException(status_code=401, detail="Authentication required")

    readings = get_user_glucose_readings(session, current_user.id, skip=skip, limit=limit)
    return readings

@router.get("/{reading_id}", response_model=GlucoseTrackerRead)
def read_reading(
    *,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    reading_id: int
):
    """Get a specific glucose reading by ID"""
    if not current_user or not current_user.id:
        raise HTTPException(status_code=401, detail="Authentication required")

    reading = get_glucose_reading(session, reading_id)
    if not reading:
        raise HTTPException(status_code=404, detail="Reading not found")
    if reading.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this reading")
    return reading

@router.put("/{reading_id}", response_model=GlucoseTrackerRead)
def update_reading(
    *,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    reading_id: int,
    reading_update: GlucoseTrackerUpdate
):
    """Update a glucose reading"""
    if not current_user or not current_user.id:
        raise HTTPException(status_code=401, detail="Authentication required")

    db_reading = get_glucose_reading(session, reading_id)
    if not db_reading:
        raise HTTPException(status_code=404, detail="Reading not found")
    if db_reading.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this reading")

    update_data = reading_update.dict(exclude_unset=True)
    return update_glucose_reading(session, db_reading, update_data)

@router.delete("/{reading_id}")
def delete_reading(
    *,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    reading_id: int
):
    """Delete a glucose reading"""
    if not current_user or not current_user.id:
        raise HTTPException(status_code=401, detail="Authentication required")

    db_reading = get_glucose_reading(session, reading_id)
    if not db_reading:
        raise HTTPException(status_code=404, detail="Reading not found")
    if db_reading.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this reading")

    return delete_glucose_reading(session, db_reading)
