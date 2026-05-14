from sqlalchemy.orm import Session
from sqlalchemy import func
from app import models,schemas

def create_transaction(db:Session,transaction:schemas.TransactionCreate):
  db_transaction=models.Transaction(
    title=transaction.title,
    amount=transaction.amount,
    category=transaction.category,
    type=transaction.type,
    date=transaction.date,
    description=transaction.description
  )
  db.add(db_transaction)
  db.commit()
  db.refresh(db_transaction)
  return db_transaction

def get_transactions(
    db: Session,
    category: str = None,
    t_type: models.TransactionType = None,
    sort=None):
    query = db.query(models.Transaction)
    if category:
        query = query.filter(models.Transaction.category == category)
    if t_type:
        query = query.filter(models.Transaction.type == t_type)
    if sort=="amount":
       query=query.order_by(models.Transaction.amount)
    if sort=="date":
       query=query.order_by(models.Transaction.date)
    return query.all()

def get_transaction(t_id:int,db:Session):
  return (db.query(models.Transaction)
          .filter(models.Transaction.id==t_id)
          .first()
          )

def delete_trans(db:Session,t_id:int):
  db_trans=db.query(models.Transaction).filter(models.Transaction.id==t_id).first()
  if db_trans:
    db.delete(db_trans)
    db.commit()
  return db_trans

def update_trans(db: Session, t_id: int, transaction: schemas.TransactionUpdate):
    db_trans = (
        db.query(models.Transaction)
        .filter(models.Transaction.id == t_id)
        .first()
    )

    if db_trans:
        db_trans.title = transaction.title
        db_trans.amount = transaction.amount
        db_trans.category = transaction.category
        db_trans.type = transaction.type
        db_trans.date = transaction.date
        db_trans.description = transaction.description

        db.commit()
        db.refresh(db_trans)

    return db_trans

from sqlalchemy import func

from sqlalchemy import func

def get_summary(db: Session, month: int = None):

    income_query = db.query(func.sum(models.Transaction.amount)).filter(
        models.Transaction.type == models.TransactionType.INCOME
    )

    expense_query = db.query(func.sum(models.Transaction.amount)).filter(
        models.Transaction.type == models.TransactionType.EXPENSE
    )

    if month:
        income_query = income_query.filter(
            func.extract('month', models.Transaction.date) == month
        )

        expense_query = expense_query.filter(
            func.extract('month', models.Transaction.date) == month
        )

    total_income = income_query.scalar() or 0
    total_expense = expense_query.scalar() or 0

    balance = total_income - total_expense

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": balance
    }


def get_category_summary(db: Session):

    summary = (
        db.query(
            models.Transaction.category,
            func.sum(models.Transaction.amount).label("total")
        )
        .filter(models.Transaction.type == models.TransactionType.EXPENSE)
        .group_by(models.Transaction.category)
        .all()
    )

    return [
        {
            "category": item.category,
            "total": item.total
        }
        for item in summary
    ]