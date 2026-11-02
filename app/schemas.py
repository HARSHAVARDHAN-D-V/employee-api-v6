from typing import Optional
from pydantic import BaseModel


class EmployeeCreate(BaseModel):
    emp_no: str
    name: str
    dept: str
    salary: float


class EmployeeReplace(BaseModel):
    name: str
    dept: str
    salary: float


class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    dept: Optional[str] = None
    salary: Optional[float] = None