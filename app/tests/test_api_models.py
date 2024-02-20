import pytest
from ..api.models import Department, HiredEmployee, Job


mock_accepted_department = ["1", "Testing Department"]

rejected_departments = [
    ["Av 123", "Failed Department"],
]

mock_accepted_hired_employee = ["1", "Employee Name", "2021-01-01T00:00:00Z", 12, 12]


rejected_employees = [
    ["Av 123", "Employee Name", "ABC", 12, 12],
    ["1", "Employee Name", "2021-01-01T00:00:00Z", "Av 123", 12],
    ["1", "Employee Name", "2021-01-01T00:00:00Z", 12, "Av 123"],
    ["1", "Employee Name", 12, 12, 12],
    ["1", 12, "2021-01-01T00:00:00Z", 12, 12],
]

mock_accepted_job = [1, "Test job"]

rejected_jobs = [
    ["Av 123", "Test Job"],
    [12, 12],
    ["Av 123", "Test Job" ]
]


def test_api_departments_model():
    assert Department(*mock_accepted_department)

    for rejected in rejected_departments:
        with pytest.raises(ValueError) as excinfo:
            Department(*rejected)
        assert excinfo.type is ValueError


def test_api_hired_employees_model():
    assert HiredEmployee(*mock_accepted_hired_employee)

    for rejected in rejected_employees:
        with pytest.raises(ValueError) as excinfo:
            HiredEmployee(*rejected)
        assert excinfo.type is ValueError


def test_api_jobs_model():
    assert Job(*mock_accepted_job)

    for rejected in rejected_jobs:
        with pytest.raises(ValueError) as excinfo:
            Job(*rejected)
        assert excinfo.type is ValueError
