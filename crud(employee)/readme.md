# Employee Management API

A simple REST API built with **FastAPI** and **SQLAlchemy** for managing employee records, backed by a SQLite database.

---

## Project Structure

```
├── main.py        # FastAPI app and route definitions
├── crud.py        # Database operations (Create, Read, Update, Delete)
├── models.py      # SQLAlchemy ORM models
├── schemas.py     # Pydantic schemas for request/response validation
├── database.py    # Database connection and session setup
```

---

## Requirements

- Python 3.8+
- FastAPI
- SQLAlchemy
- Uvicorn
- Pydantic[email]

---

## Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd <project-folder>
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate        # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install fastapi sqlalchemy uvicorn pydantic[email]
   ```

---

## Running the Server

```bash
uvicorn main:app --reload
```

The API will be available at: `http://127.0.0.1:8000`

Interactive docs (Swagger UI): `http://127.0.0.1:8000/docs`

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/employee` | Create a new employee |
| `GET` | `/employees` | Get all employees |
| `GET` | `/employees/{emp_id}` | Get a single employee by ID |
| `PUT` | `/employee/{emp_id}` | Update an employee by ID |
| `DELETE` | `/employees/{emp_id}` | Delete an employee by ID |

---

## Request & Response Examples

### Create Employee — `POST /employee`

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john.doe@example.com"
}
```

**Response:**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john.doe@example.com"
}
```

---

### Get All Employees — `GET /employees`

**Response:**
```json
[
  {
    "id": 1,
    "name": "John Doe",
    "email": "john.doe@example.com"
  }
]
```

---

### Get Single Employee — `GET /employees/{emp_id}`

**Response:**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john.doe@example.com"
}
```

Returns `404 Not Found` if the employee does not exist.

---

### Update Employee — `PUT /employee/{emp_id}`

**Request Body:**
```json
{
  "name": "Jane Doe",
  "email": "jane.doe@example.com"
}
```

**Response:**
```json
{
  "id": 1,
  "name": "Jane Doe",
  "email": "jane.doe@example.com"
}
```

Returns `404 Not Found` if the employee does not exist.

---

### Delete Employee — `DELETE /employees/{emp_id}`

**Response:**
```json
{
  "id": 1,
  "name": "Jane Doe",
  "email": "jane.doe@example.com"
}
```

Returns `404 Not Found` if the employee does not exist.

---

## Database

The app uses **SQLite** with a local file `test.db`, created automatically on first run. No additional database setup is required.

To use a different database (e.g., PostgreSQL), update the connection URL in `database.py`:
```python
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/dbname"
```

---

## Notes

- `email` must be a valid email format and is unique per employee.
- The `schemas.py` `EmployeeOut` class uses `orm_mode = True` — note the config class name should be `Config` (capital C) for Pydantic v1, or use `model_config` for Pydantic v2.