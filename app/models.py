from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Item(BaseModel):
    name: str
    email: str
    item_name: str
    quantity: int
    expiry_date: datetime

class ClockInRecord(BaseModel):
    email: str
    location: str