from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from glucose_tracker.models import GlucoseTracker

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    age: int
    diabetes_type: int
    email: str = Field(index=True, unique=True)
    phone: str
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship with GlucoseTracker
    glucose_readings: List["GlucoseTracker"] = Relationship(back_populates="user")
