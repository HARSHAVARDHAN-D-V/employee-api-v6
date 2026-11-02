from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import SessionLocal
from app.repositories.employee_repository import EmployeeRepository
from app.responses import BAD_REQUEST_RESPONSE, DUPLICATE_RESPONSE, NOT_FOUND_RESPONSE
from app.schemas import EmployeeCreate, EmployeeReplace, EmployeeUpdate
from app.services.employee_service import EmployeeService

router = APIRouter(prefix="/employee", tags=["employee"])


async def get_db():
    async with SessionLocal() as db:
        yield db


def get_service(db: AsyncSession = Depends(get_db)) -> EmployeeService:
    return EmployeeService(EmployeeRepository(db))


@router.get("/")
async def list_employees(service: EmployeeService = Depends(get_service)):
    return await service.list_employees()


@router.get("/{emp_no}", responses=NOT_FOUND_RESPONSE)
async def get_employee(emp_no: str, service: EmployeeService = Depends(get_service)):
    return await service.get_employee(emp_no)


@router.post(
    "/",
    status_code=201,
    responses=DUPLICATE_RESPONSE | BAD_REQUEST_RESPONSE,
)
async def create_employee(
    data: EmployeeCreate, service: EmployeeService = Depends(get_service)
):
    return await service.create_employee(data)


@router.put("/{emp_no}", responses=NOT_FOUND_RESPONSE | BAD_REQUEST_RESPONSE)
async def replace_employee(
    emp_no: str, data: EmployeeReplace, service: EmployeeService = Depends(get_service)
):
    return await service.replace_employee(emp_no, data)


@router.patch("/{emp_no}", responses=NOT_FOUND_RESPONSE | BAD_REQUEST_RESPONSE)
async def update_employee(
    emp_no: str, data: EmployeeUpdate, service: EmployeeService = Depends(get_service)
):
    return await service.update_employee(emp_no, data)


@router.delete("/{emp_no}", responses=NOT_FOUND_RESPONSE)
async def delete_employee(emp_no: str, service: EmployeeService = Depends(get_service)):
    await service.delete_employee(emp_no)
    return {"message": f"Employee {emp_no} deleted"}