from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from auth_service.models import User

class GlucoseTrackerBase(SQLModel):
    level: float
    time: datetime
    before_after_bed: str  # "before", "after", or "none"
    user_id: int = Field(foreign_key="user.id")

class GlucoseTracker(GlucoseTrackerBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # Relationship with User
    user: "User" = Relationship(back_populates="glucose_readings")

class GlucoseTrackerCreate(GlucoseTrackerBase):
    pass

class GlucoseTrackerRead(GlucoseTrackerBase):
    id: int

class GlucoseTrackerUpdate(SQLModel):
    level: Optional[float] = None
    time: Optional[datetime] = None
    before_after_bed: Optional[str] = None
