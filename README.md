# Employee API

A CRUD API for employee records, built with FastAPI and PostgreSQL (async), using a layered structure: router -> service -> repository -> database.

## Tech Stack
Python 3.14, FastAPI, SQLAlchemy (async) with asyncpg, PostgreSQL, uv

## Prerequisites
- Python 3.14+ (`python3 --version`)
- PostgreSQL running locally (`pg_isready` should say "accepting connections")
- uv (`uv --version`). If missing: `curl -LsSf https://astral.sh/uv/install.sh | sh`, then restart the terminal.

## Setup (first time only)
1. Go into the project folder: `cd employee_api_v6`
2. Install dependencies: `uv sync`
3. Create the database and table:
   ```
   psql -d postgres -c "CREATE DATABASE employee_v6;"
   psql -d employee_v6 -c "CREATE TABLE employee (id SERIAL PRIMARY KEY, emp_no VARCHAR(6) UNIQUE NOT NULL, name VARCHAR(100) NOT NULL, dept VARCHAR(50), salary NUMERIC(10, 2));"
   ```
   (No `psql`? Run the same SQL in pgAdmin's Query Tool.)
4. Open `app/database.py` and set `DATABASE_URL` to your own Postgres user and database:
   `postgresql+asyncpg://YOUR_USER@localhost:5432/employee_v6`
   (With a password: `YOUR_USER:YOUR_PASSWORD@`)

## Run
```
uv run uvicorn main:app --reload
```
Wait for `Application startup complete.`, then open http://127.0.0.1:8000/docs

## Endpoints
`emp_no` format: `E` followed by 5 digits (e.g. `E00001`). Lowercase input is converted to uppercase. It is set on creation and cannot be changed later.

| Method | Endpoint | Description |
|---|---|---|
| GET | /employee/ | List all employees |
| GET | /employee/{emp_no} | Get one employee |
| POST | /employee/ | Create an employee (201) |
| PUT | /employee/{emp_no} | Replace name, dept, salary (all required) |
| PATCH | /employee/{emp_no} | Update only the fields sent |
| DELETE | /employee/{emp_no} | Delete an employee |

Example POST body:
```json
{"emp_no": "E00006", "name": "Divya", "dept": "HR", "salary": 42000}
```

## Errors
| Status | Meaning |
|---|---|
| 400 | Bad emp_no format, salary not positive, or no fields provided |
| 404 | No employee with that emp_no |
| 409 | An employee with that emp_no already exists |
| 422 | Malformed body (e.g. salary sent as text) |

## Project structure
```
app/
  database.py        async engine and session
  models.py          SQLAlchemy table
  schemas.py         request shapes (Pydantic)
  exceptions.py      our own error types
  responses.py       error docs for /docs
  repositories/      database access only
  services/          business rules only
  routers/           HTTP only
main.py              app entry point and error-to-status mapping
```

## Troubleshooting
- **Address already in use:** `lsof -i :8000`, then `kill -9 <PID>`.
- **No module named ...:** run `uv sync` and start with `uv run uvicorn ...`.
- **Connection errors:** check `pg_isready`, and that the database name and user in `app/database.py` match.