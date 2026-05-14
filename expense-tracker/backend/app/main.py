from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, SessionLocal, Base
from app import schemas, models, crud

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ── Static-path routes FIRST (before any /{t_id} routes) ──────────────────

# Get Summary
@app.get("/transactions/summary", response_model=schemas.SummaryBase)
def get_summary(
    month: int = None,
    db: Session = Depends(get_db)
):
    if month and (month < 1 or month > 12):
        raise HTTPException(
            status_code=400,
            detail="Month must be between 1 and 12"
        )
    return crud.get_summary(db, month)


# Get Category Summary
@app.get("/transactions/category-summary", response_model=List[schemas.CategorySummary])
def category_summary(db: Session = Depends(get_db)):
    return crud.get_category_summary(db)


# ── General collection routes ──────────────────────────────────────────────

# Create Transaction
@app.post("/transactions", response_model=schemas.TransactionOut)
def create_transaction(
    transaction: schemas.TransactionCreate,
    db: Session = Depends(get_db)
):
    return crud.create_transaction(db, transaction)


# Get All Transactions
@app.get("/transactions", response_model=List[schemas.TransactionOut])
def get_transactions(
    category: str = None,
    t_type: models.TransactionType = None,
    sort=None,
    db: Session = Depends(get_db)
):
    return crud.get_transactions(db, category, t_type, sort)


# ── Dynamic /{t_id} routes LAST ────────────────────────────────────────────

# Get Single Transaction
@app.get("/transactions/{t_id}", response_model=schemas.TransactionOut)
def get_transaction(t_id: int, db: Session = Depends(get_db)):
    tran = crud.get_transaction(t_id, db)
    if tran is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return tran


# Update Transaction
@app.put("/transactions/{t_id}", response_model=schemas.TransactionOut)
def update_transaction(
    t_id: int,
    transaction: schemas.TransactionUpdate,
    db: Session = Depends(get_db)
):
    tran = crud.update_trans(db, t_id, transaction)
    if tran is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return tran


# Delete Transaction
@app.delete("/transactions/{t_id}", response_model=schemas.TransactionOut)
def delete_transaction(t_id: int, db: Session = Depends(get_db)):
    tran = crud.delete_trans(db, t_id)
    if tran is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return tran