from sqlalchemy import DeclarativeBase, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class HiredEmployees(Base):
    __tablename__ = "hired_employees"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    datetime: str
    department_id: Mapped[int] = ForeignKey("departments.id")
    job_id: Mapped[int] = ForeignKey("jobs.id")


class Departments(Base):
    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(primary_key=True)
    department: Mapped[str]


class Jobs(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(primary_key=True)
    job: Mapped[str]

