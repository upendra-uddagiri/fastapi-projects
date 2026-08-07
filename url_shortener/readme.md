# URL Shortener API

A simple RESTful URL Shortener API built using **FastAPI**, **SQLite**, and **SQLAlchemy**.

---

## Features

* Shorten long URLs
* Redirect using short codes
* Track click counts
* View URL statistics
* SQLite database for persistent storage
* Interactive Swagger UI

---

## Tech Stack

* FastAPI
* SQLAlchemy
* SQLite
* Pydantic
* Uvicorn

---

## Project Structure

```text
url_shortener/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── routers.py
│   └── utils.py
│
├── requirements.txt
├── README.md
└── url_shortener.db
```

---

## Installation

### Clone the repository

```bash
git clone <repository-url>
cd url_shortener
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run the Application

```bash
uvicorn app.main:app --reload
```

Application

```
http://127.0.0.1:8000
```

Swagger Documentation

```
http://127.0.0.1:8000/docs
```

ReDoc

```
http://127.0.0.1:8000/redoc
```

---

## API Endpoints

### Home

```
GET /
```

Response

```json
{
  "message": "URL Shortener API is Running"
}
```

---

### Shorten URL

```
POST /shorten
```

Request

```json
{
  "original_url": "https://www.google.com"
}
```

Response

```json
{
  "short_code": "Ab12Cd",
  "short_url": "http://localhost:8000/Ab12Cd"
}
```

---

### Redirect

```
GET /{short_code}
```

Example

```
GET /Ab12Cd
```

Automatically redirects to

```
https://www.google.com
```

---

### URL Statistics

```
GET /stats/{short_code}
```

Response

```json
{
  "original_url": "https://www.google.com/",
  "short_code": "Ab12Cd",
  "clicks": 5,
  "created_at": "2026-08-06T18:40:12.123456"
}
```

---

## Database Schema

| Column       | Type     | Description         |
| ------------ | -------- | ------------------- |
| id           | Integer  | Primary Key         |
| original_url | String   | Original Long URL   |
| short_code   | String   | Unique Short Code   |
| clicks       | Integer  | Number of Redirects |
| created_at   | DateTime | Creation Timestamp  |

---

## Workflow

1. User sends a long URL.
2. API generates a unique short code.
3. URL is stored in SQLite.
4. API returns the shortened URL.
5. Visiting the short URL redirects to the original URL.
6. Click count is incremented on every redirect.
7. Statistics can be retrieved using the stats endpoint.

---

## Future Improvements

* Custom short aliases
* QR Code generation
* URL expiration
* User authentication
* Rate limiting
* Analytics dashboard
* Docker support
* PostgreSQL support
* Redis caching
* Unit & Integration tests

---

## Author

Developed using FastAPI and SQLAlchemy as a learning project.
