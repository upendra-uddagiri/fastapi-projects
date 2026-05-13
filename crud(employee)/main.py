from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from database import engine, SessionLocal, Base
import models
import schemas
import crud


# Create tables
Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI()


# Database dependency
def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# 1. Create employee
@app.post(
    "/employee",
    response_model=schemas.EmployeeOut
)
def create_employee(
    employee: schemas.EmployeeCreate,
    db: Session = Depends(get_db)
):
    return crud.create_employee(db, employee)


# 2. Get all employees
@app.get(
    "/employees",
    response_model=List[schemas.EmployeeOut]
)
def get_employees(
    db: Session = Depends(get_db)
):
    return crud.get_employees(db)


# 3. Get single employee
@app.get(
    "/employees/{emp_id}",
    response_model=schemas.EmployeeOut
)
def get_employee(
    emp_id: int,
    db: Session = Depends(get_db)
):
    employee = crud.get_employee(db, emp_id)

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee Not Found"
        )

    return employee


# 4. Update employee
@app.put(
    "/employee/{emp_id}",
    response_model=schemas.EmployeeOut
)
def update_employee(
    emp_id: int,
    employee: schemas.EmployeeUpdate,
    db: Session = Depends(get_db)
):
    db_employee = crud.update_employee(
        db,
        emp_id,
        employee
    )

    if db_employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee Not Found"
        )

    return db_employee


# 5. Delete employee
@app.delete(
    "/employees/{emp_id}",
    response_model=schemas.EmployeeOut
)
def delete_employee(
    emp_id: int,
    db: Session = Depends(get_db)
):
    employee = crud.delete_employee(db, emp_id)

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee Not Found"
        )

    return employee
