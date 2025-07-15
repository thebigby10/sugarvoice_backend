from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class GlucoseReadingBase(BaseModel):
    level: float
    time: datetime
    before_after_bed: str

class GlucoseReadingCreate(GlucoseReadingBase):
    pass

class GlucoseReadingRead(GlucoseReadingBase):
    id: int
    user_id: int

class GlucoseReadingUpdate(BaseModel):
    level: Optional[float] = None
    time: Optional[datetime] = None
    before_after_bed: Optional[str] = None
