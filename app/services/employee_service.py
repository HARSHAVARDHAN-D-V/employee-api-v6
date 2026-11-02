import re

from app.exceptions import EmployeeNotFoundError, InvalidEmployeeDataError
from app.models import Employee
from app.repositories.employee_repository import EmployeeRepository
from app.schemas import EmployeeCreate, EmployeeReplace, EmployeeUpdate

EMP_NO_PATTERN = re.compile(r"^E\d{5}$")


class EmployeeService:
    def __init__(self, repo: EmployeeRepository):
        self.repo = repo

    @staticmethod
    def _clean_emp_no(emp_no: str) -> str:
        return emp_no.strip().upper()

    @staticmethod
    def _validate_emp_no(emp_no: str) -> None:
        if not EMP_NO_PATTERN.match(emp_no):
            raise InvalidEmployeeDataError(
                "emp_no must be 'E' followed by 5 digits, e.g. E00001"
            )

    @staticmethod
    def _validate_salary(salary: float) -> None:
        if salary <= 0:
            raise InvalidEmployeeDataError("salary must be greater than 0")

    async def list_employees(self):
        return await self.repo.get_all()

    async def get_employee(self, emp_no: str):
        employee = await self.repo.get_by_emp_no(self._clean_emp_no(emp_no))
        if employee is None:
            raise EmployeeNotFoundError()
        return employee

    async def create_employee(self, data: EmployeeCreate):
        emp_no = self._clean_emp_no(data.emp_no)
        self._validate_emp_no(emp_no)
        self._validate_salary(data.salary)
        employee = Employee(
            emp_no=emp_no, name=data.name, dept=data.dept, salary=data.salary
        )
        return await self.repo.add(employee)

    async def replace_employee(self, emp_no: str, data: EmployeeReplace):
        self._validate_salary(data.salary)
        updated = await self.repo.update(
            self._clean_emp_no(emp_no),
            {"name": data.name, "dept": data.dept, "salary": data.salary},
        )
        if updated is None:
            raise EmployeeNotFoundError()
        return updated

    async def update_employee(self, emp_no: str, data: EmployeeUpdate):
        values = data.model_dump(exclude_unset=True, exclude_none=True)
        if not values:
            raise InvalidEmployeeDataError("No fields provided")
        if "salary" in values:
            self._validate_salary(values["salary"])
        updated = await self.repo.update(self._clean_emp_no(emp_no), values)
        if updated is None:
            raise EmployeeNotFoundError()
        return updated

    async def delete_employee(self, emp_no: str):
        employee = await self.get_employee(emp_no)
        await self.repo.delete(employee)
        