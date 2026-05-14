# Expense Tracker

A full-stack personal finance tracker built with **FastAPI** (backend) and **HTML/CSS/JS** (frontend). Track your income and expenses, filter transactions, and view category-wise spending breakdowns.

---

## Project Structure

```
project/
│
├── app/
│   ├── main.py         # FastAPI app, routes, and middleware
│   ├── crud.py         # Database query logic
│   ├── database.py     # SQLAlchemy engine and session setup
│   ├── models.py       # ORM models (Transaction, TransactionType)
│   └── schemas.py      # Pydantic schemas for request/response validation
│
├── frontend/
│   ├── index.html      # App structure and markup
│   ├── style.css       # Styles, layout, and theming
│   └── script.js       # API calls, rendering, and interactions
│
├── test.db             # SQLite database (auto-created on first run)
└── README.md
```

---

## Features

- Add, edit, and delete transactions
- Filter by category, type (income/expense), and sort by date or amount
- Dashboard with income/expense summary and category bar chart
- Monthly summary filter
- Expense breakdown by category
- Fully responsive UI

---

## Tech Stack

| Layer    | Technology                        |
|----------|-----------------------------------|
| Backend  | Python, FastAPI, SQLAlchemy       |
| Database | SQLite                            |
| Frontend | HTML, CSS, Vanilla JavaScript     |

---

## Getting Started

### Prerequisites

- Python 3.8+
- pip

### 1. Clone the repository

```bash
git clone https://github.com/upedra-uddagiri/fastapi-projects/expense-tracker.git
cd expense-tracker
```

### 2. Install dependencies

```bash
pip install fastapi uvicorn sqlalchemy pydantic
```

### 3. Run the backend

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

### 4. Run the frontend

Open `frontend/index.html` with **Live Server** (VS Code extension) on port `5500`.

Or install Live Server globally:

```bash
npm install -g live-server
cd frontend
live-server --port=5500
```

Then visit `http://127.0.0.1:5500`.

---

## API Reference

Base URL: `http://127.0.0.1:8000`

### Transactions

| Method | Endpoint                          | Description                        |
|--------|-----------------------------------|------------------------------------|
| GET    | `/transactions`                   | Get all transactions (with filters)|
| POST   | `/transactions`                   | Create a new transaction           |
| GET    | `/transactions/{id}`              | Get a single transaction           |
| PUT    | `/transactions/{id}`              | Update a transaction               |
| DELETE | `/transactions/{id}`              | Delete a transaction               |
| GET    | `/transactions/summary`           | Get income/expense/balance totals  |
| GET    | `/transactions/category-summary`  | Get expense totals per category    |

### Query Parameters for `GET /transactions`

| Parameter  | Type   | Description                        |
|------------|--------|------------------------------------|
| `category` | string | Filter by category name            |
| `t_type`   | string | Filter by `income` or `expense`    |
| `sort`     | string | Sort by `date` or `amount`         |

### Query Parameters for `GET /transactions/summary`

| Parameter | Type | Description               |
|-----------|------|---------------------------|
| `month`   | int  | Filter by month (1 to 12) |

### Example Request Body (POST / PUT)

```json
{
  "title": "Grocery run",
  "amount": 850.00,
  "category": "Food",
  "type": "expense",
  "date": "2025-05-14T10:30:00",
  "description": "Weekly groceries"
}
```

---

## Environment Notes

- The SQLite database (`test.db`) is created automatically when the server starts for the first time.
- CORS is configured to allow requests from `http://127.0.0.1:5500` and `http://localhost:5500` (default Live Server ports).
- If you change the frontend port, update `allow_origins` in `main.py` accordingly.

---

## Interactive API Docs

FastAPI provides auto-generated docs at:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

---

## Known Issues Fixed

- `/transactions/summary` and `/transactions/category-summary` routes must be declared **before** `/transactions/{t_id}` in `main.py` to prevent FastAPI from matching the static path segments as integer path parameters (causing 422 errors).

---