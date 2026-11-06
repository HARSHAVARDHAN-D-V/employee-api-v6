# Employee API

A beginner-friendly REST API for managing employee records. It is built with
FastAPI and PostgreSQL, uses async database access, and is organised in layers:

    router -> service -> repository -> database

- **Router**: handles HTTP only (URLs, status codes).
- **Service**: holds the business rules (emp_no format, salary must be positive).
- **Repository**: talks to the database only.

This guide assumes you have never seen the project. Follow the steps in order
and do not skip any. Everything is explained as we go.

---

## 1. What you need installed

You need three things on your computer: Python 3.14+, PostgreSQL, and uv.
Check each one by typing the command in a terminal.

(On a Mac, open the "Terminal" app. On Windows, use PowerShell.)

### 1.1 Python 3.14 or newer

    python3 --version

You should see `Python 3.14.x` or higher. If you have an older version, do not
worry: uv (below) will normally download the right Python for you
automatically. If that fails, install Python from https://www.python.org/downloads/

### 1.2 PostgreSQL (the database)

    pg_isready

You should see `accepting connections`. If you see "command not found" or "no
response", PostgreSQL is either not installed or not running.

- Install: https://www.postgresql.org/download/ (on Mac, Postgres.app is the
  easiest: https://postgresapp.com)
- Make sure it is running. With Postgres.app, open the app and click
  "Start". It keeps running in the background after that.

### 1.3 uv (manages Python packages for this project)

    uv --version

You should see a version number. If not, install it:

    curl -LsSf https://astral.sh/uv/install.sh | sh

(On Windows PowerShell:
`powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`)

Then **close the terminal and open a new one**, and run `uv --version` again.

---

## 2. Get the project

1. Unzip the project zip file into a folder, for example `employee_api`.
2. Open a terminal and go into that folder:

       cd path/to/employee_api

3. Check that the files are there. Use the `-a` flag so hidden files show up:

       ls -la

You should see these (the ones starting with a dot are hidden files and are
required):

    .python-version
    .gitignore
    README.md
    app/
    main.py
    pyproject.toml
    uv.lock

If `.python-version` is missing, create it:

    echo "3.14" > .python-version

---

## 3. Install the project's packages

From inside the project folder, run:

    uv sync

This reads `pyproject.toml` and `uv.lock`, creates a private environment in a
folder called `.venv`, and installs exactly the packages this project needs
(FastAPI, SQLAlchemy, asyncpg, and others). It can take a minute.

You do not need to "activate" anything. From now on, always put `uv run` in
front of commands so they run inside that private environment.

---

## 4. Create the database and table

The app does **not** create its own table. You create it once, by hand.

First, pick a name for your database. This guide uses `employee_db`, but you
can use any name. Remember it, because you will need it again in step 5.

### 4.1 Option A: using the terminal (psql)

    psql -d postgres -c "CREATE DATABASE employee_db;"

Then create the table inside it:

    psql -d employee_db -c "CREATE TABLE employee (id SERIAL PRIMARY KEY, emp_no VARCHAR(6) UNIQUE NOT NULL, name VARCHAR(100) NOT NULL, dept VARCHAR(50), salary NUMERIC(10, 2));"

Check that it worked:

    psql -d employee_db -c "\d employee"

You should see a table with the columns: id, emp_no, name, dept, salary.

If you see `command not found: psql`, use Option B instead.

### 4.2 Option B: using pgAdmin (a visual tool)

1. Open pgAdmin and connect to your local server.
2. Right-click **Databases** -> **Create** -> **Database...**, enter the name
   `employee_db`, and click Save.
3. Right-click your new database -> **Query Tool**.
4. Paste this and click the Run (play) button:

       CREATE TABLE employee (
           id SERIAL PRIMARY KEY,
           emp_no VARCHAR(6) UNIQUE NOT NULL,
           name VARCHAR(100) NOT NULL,
           dept VARCHAR(50),
           salary NUMERIC(10, 2)
       );

### What the columns mean

| Column | Meaning |
|---|---|
| id | Internal number the database assigns automatically. You never set it. |
| emp_no | The employee number you use everywhere, like `E00001`. Must be unique. |
| name | Employee name. |
| dept | Department. |
| salary | Salary, up to 2 decimal places. |

---

## 5. Tell the app how to reach your database (the one file you must edit)

Open `app/database.py`. Find this line:

    DATABASE_URL = "postgresql+asyncpg://harshav007@localhost:5432/employee_v6"

Change it to match **your** setup. The pattern is:

    postgresql+asyncpg://USERNAME@localhost:5432/DATABASE_NAME

- **USERNAME**: your PostgreSQL user.
  - On a Mac with Postgres.app, this is usually your Mac username. Find it with:

        whoami

  - If you installed PostgreSQL with the official installer, the user is
    usually `postgres`.
- **DATABASE_NAME**: the name you chose in step 4 (for example `employee_db`).

If your PostgreSQL user has a password, write it like this:

    postgresql+asyncpg://USERNAME:PASSWORD@localhost:5432/DATABASE_NAME

Example:

    DATABASE_URL = "postgresql+asyncpg://postgres:mypassword@localhost:5432/employee_db"

Save the file.

---

## 6. Start the server

From the project folder:

    uv run uvicorn main:app --reload

Wait until you see this line:

    INFO:     Application startup complete.

The server is now running. **Leave this terminal window open.** The server only
runs while this window is open and the command is running.

To stop it later, click on the terminal and press `Ctrl + C`.

---

## 7. Try it out

Open your browser and go to:

    http://127.0.0.1:8000/docs

This page (called Swagger UI) lists every endpoint. To try one: click it ->
**Try it out** -> fill in the fields -> **Execute**. The response appears
below.

### Suggested first test

1. **POST /employee/** with this body:

       {"emp_no": "E00001", "name": "Ram", "dept": "CSE", "salary": 10000}

   Expected: status **201**, and the employee is returned with an `id`.

2. **GET /employee/** -> expected: a list containing Ram.
3. **GET /employee/E00001** -> expected: Ram's record.
4. **PATCH /employee/E00001** with `{"salary": 12000}` -> expected: only the
   salary changes.
5. **DELETE /employee/E00001** -> expected: a "deleted" message.
6. **GET /employee/E00001** again -> expected: status **404**.

---

## 8. Endpoint reference

| Method | URL | What it does |
|---|---|---|
| GET | /employee/ | List all employees |
| GET | /employee/{emp_no} | Get one employee |
| POST | /employee/ | Create an employee |
| PUT | /employee/{emp_no} | Replace name, dept and salary (all three required) |
| PATCH | /employee/{emp_no} | Change only the fields you send |
| DELETE | /employee/{emp_no} | Delete an employee |

### Rules the API enforces

- **emp_no format:** the letter `E` followed by exactly 5 digits (`E00001`).
  Lowercase is accepted and converted (`e00001` becomes `E00001`).
- **emp_no is permanent:** you set it when creating an employee and cannot
  change it afterwards.
- **emp_no must be unique:** two employees cannot share one.
- **salary must be greater than 0.**

### Example request bodies

Create (POST):

    {"emp_no": "E00002", "name": "Divya", "dept": "HR", "salary": 42000}

Replace (PUT). All three fields are required:

    {"name": "Divya", "dept": "Finance", "salary": 50000}

Update (PATCH). Send only what you want to change:

    {"salary": 45000}

---

## 9. Error responses

| Status | Meaning | Example cause |
|---|---|---|
| 400 | Request breaks a rule | Bad emp_no like `X1`, salary of -5, or an empty PATCH body |
| 404 | Employee not found | GET/PUT/PATCH/DELETE on an emp_no that does not exist |
| 409 | Already exists | POST with an emp_no that is already taken |
| 422 | Wrong data type | Sending salary as text like `"abc"` |

Error responses look like this:

    {"detail": "Employee not found"}

---

## 10. How the project is organised

    employee_api/
    ├── main.py                  Starts the app; turns our errors into HTTP status codes
    ├── pyproject.toml           List of packages the project needs
    ├── uv.lock                  Exact package versions (keeps installs identical)
    ├── .python-version          Which Python version to use
    └── app/
        ├── database.py          Connection to PostgreSQL
        ├── models.py            The employee table, described in Python
        ├── schemas.py           The JSON shapes the API accepts
        ├── exceptions.py        Our own error types (not found, duplicate, invalid)
        ├── responses.py         Error descriptions shown in /docs
        ├── routers/
        │   └── employee.py      URLs only; passes work to the service
        ├── services/
        │   └── employee_service.py   Business rules
        └── repositories/
            └── employee_repository.py   All database queries

### What happens during one request (GET /employee/E00001)

1. Your browser sends the request to the server.
2. The **router** receives it and calls the service.
3. The **service** cleans the emp_no and asks the repository for that employee.
4. The **repository** runs the database query and returns the result.
5. If nothing was found, the service raises "not found", and `main.py` turns
   it into a 404.
6. Otherwise the employee goes back up and is sent as JSON.

---

## 11. Troubleshooting

**"Address already in use" when starting the server**
Another copy is still running on port 8000. Find and stop it:

    lsof -i :8000
    kill -9 <the PID number shown>

Then start the server again.

**"No module named ..." or "command not found: uvicorn"**
You ran the command without `uv run`, or skipped `uv sync`. Run `uv sync`, then
start with exactly: `uv run uvicorn main:app --reload`

**"password authentication failed" or "role does not exist"**
The username in `app/database.py` is wrong for your PostgreSQL, or it needs a
password. Recheck step 5.

**"database ... does not exist"**
The database name in `app/database.py` does not match the one you created.
List your databases with `psql -l` or look in pgAdmin.

**"relation employee does not exist"**
You created the database but not the table. Redo step 4 (the CREATE TABLE part)
on the correct database.

**"connection refused" on port 5432**
PostgreSQL is not running. Start it (for Postgres.app, open the app and click
Start), then check with `pg_isready`.

**The browser says it can't connect to 127.0.0.1:8000**
The server is not running. Go back to step 6. It does not start by itself, and
it stops when you close the terminal.

**I can't see .python-version or .gitignore**
They are hidden files. Use `ls -la` in the terminal, or press
`Cmd + Shift + .` in Finder to show hidden files.

---

## 12. Quick reference (after the first-time setup)

Every later time you want to run the project:

    cd path/to/employee_api
    uv run uvicorn main:app --reload

Then open http://127.0.0.1:8000/docs
