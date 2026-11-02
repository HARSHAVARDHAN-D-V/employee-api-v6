from sqlalchemy import Column, Integer, String, Numeric
from app.database import Base


class Employee(Base):
    __tablename__ = "employee"

    id = Column(Integer, primary_key=True, index=True)
    emp_no = Column(String(6), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    dept = Column(String(50))
    salary = Column(Numeric(10, 2))
    