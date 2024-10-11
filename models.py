from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Item(BaseModel):
    name: str
    email: str
    item_name: str
    quantity: int
    expiry_date: datetime

class UserClockInRecord(BaseModel):
    user_id: str
    clock_in: datetime
    clock_out: Optional[datetime] = None