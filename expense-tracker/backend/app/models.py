from sqlalchemy import Column,Integer,String,Enum,DateTime,Text,Float
from app.database import Base
import enum

class TransactionType(str, enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"


class Transaction(Base):
  __tablename__="transactions"

  id=Column(Integer,primary_key=True,index=True)
  title=Column(String,index=True)
  amount=Column(Float,index=True,nullable=False)
  category=Column(String,index=True,nullable=False)
  type = Column(Enum(TransactionType), index=True, nullable=False)
  date=Column(DateTime,index=True,nullable=False)
  description=Column(Text,nullable=True)