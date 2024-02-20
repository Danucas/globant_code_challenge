from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from dataclasses import dataclass, asdict
from datetime import datetime
import traceback


class Base(DeclarativeBase):
    pass


class HiredEmployees(Base):
    __tablename__ = "hired_employees"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    datetime: Mapped[DateTime] = mapped_column(DateTime(timezone=True))
    department_id: Mapped[int] = mapped_column(
        ForeignKey("departments.id"), nullable=True
    )
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id"), nullable=True)


class Departments(Base):
    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(primary_key=True)
    department: Mapped[str]


class Jobs(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(primary_key=True)
    job: Mapped[str]


class ValidationModel:
    dict = asdict

    def __post_init__(self):
        for name, field in self.__dataclass_fields__.items():
            value = getattr(self, name)
            try:
                if field.type == datetime:
                    if isinstance(value, datetime):
                        to_type = value.strftime("%Y-%m-%dT%H:%M:%SZ")
                    elif isinstance(value, str):
                        to_type = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
                    else:
                        raise ValueError
                elif field.type == str:
                    if not isinstance(value, str):
                        raise ValueError
                    to_type = field.type(value)
                else:
                    to_type = field.type(value or 0)
                setattr(self, name, to_type)
            except Exception as e:
                print(traceback.format_exc(), name, field, value, e, type(e))
                raise e


@dataclass
class Department(ValidationModel):
    id: int
    department: str


@dataclass
class HiredEmployee(ValidationModel):
    id: int
    name: str
    datetime: datetime
    department_id: int
    job_id: int


@dataclass
class Job(ValidationModel):
    id: int
    job: str


@dataclass
class EmployeesByQuarters(ValidationModel):
    department: str
    job: str
    q1: int
    q2: int
    q3: int
    q4: int


@dataclass
class MostHiringDepartments(ValidationModel):
    id: int
    department: str
    hired: int
