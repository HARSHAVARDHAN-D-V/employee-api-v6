from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions import (
    DuplicateEmployeeError,
    EmployeeNotFoundError,
    InvalidEmployeeDataError,
)
from app.routers import employee

app = FastAPI(title="Employee API")


@app.exception_handler(EmployeeNotFoundError)
async def handle_not_found(request: Request, exc: EmployeeNotFoundError):
    return JSONResponse(status_code=404, content={"detail": "Employee not found"})


@app.exception_handler(DuplicateEmployeeError)
async def handle_duplicate(request: Request, exc: DuplicateEmployeeError):
    return JSONResponse(
        status_code=409, content={"detail": "Employee with this emp_no already exists"}
    )


@app.exception_handler(InvalidEmployeeDataError)
async def handle_invalid(request: Request, exc: InvalidEmployeeDataError):
    return JSONResponse(status_code=400, content={"detail": exc.message})


app.include_router(employee.router)