from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import DuplicateEmployeeError
from app.models import Employee


class EmployeeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self):
        result = await self.db.execute(select(Employee))
        return result.scalars().all()

    async def get_by_emp_no(self, emp_no: str):
        result = await self.db.execute(
            select(Employee).where(Employee.emp_no == emp_no)
        )
        return result.scalar_one_or_none()

    async def add(self, employee: Employee):
        self.db.add(employee)
        try:
            await self.db.commit()
        except IntegrityError:
            await self.db.rollback()
            raise DuplicateEmployeeError()
        await self.db.refresh(employee)
        return employee

    async def update(self, emp_no: str, values: dict):
        stmt = (
            update(Employee)
            .where(Employee.emp_no == emp_no)
            .values(**values)
            .returning(Employee)
        )
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.scalar_one_or_none()

    async def delete(self, employee: Employee):
        await self.db.delete(employee)
        await self.db.commit()