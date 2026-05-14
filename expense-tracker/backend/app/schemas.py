from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.models import TransactionType


# Base schema
class TransactionBase(BaseModel):
    title: str
    amount: float
    category: str
    type: TransactionType
    date: datetime
    description: Optional[str] = None


# Create schema
class TransactionCreate(TransactionBase):
    pass


# Update schema
class TransactionUpdate(BaseModel):
    title: Optional[str] = None
    amount: Optional[float] = None
    category: Optional[str] = None
    type: Optional[TransactionType] = None
    date: Optional[datetime] = None
    description: Optional[str] = None


# Response schema
class TransactionOut(TransactionBase):
    id: int

    class Config:
        orm_mode = True


# Summary schema (used by /transactions/summary)
class SummaryBase(BaseModel):
    total_income: float
    total_expense: float
    balance: float


# Category summary schema
class CategorySummary(BaseModel):
    category: str
    total: float