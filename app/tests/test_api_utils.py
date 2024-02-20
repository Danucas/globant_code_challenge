import pytest
from ..api.utils import Utils
from ..api.db_engine import ENTITY_MAP
import os
import logging

LOGGER = logging.getLogger(__name__)

from .test_api_models import (
    mock_accepted_department,
    mock_accepted_job,
    mock_accepted_hired_employee,
)
import csv


MAP = {
    "departments": mock_accepted_department,
    "jobs": mock_accepted_job,
    "hired_employees": mock_accepted_hired_employee,
}


class File:
    def __init__(self, entity) -> None:
        self.entity = entity
        self.data = [MAP.get(entity)] * 1500
        self.filename = f"test_file_{entity}.csv"

    def save(self, filename):
        with open(filename, "w+") as file:
            writer = csv.writer(file)
            for row in self.data:
                writer.writerow(row)


class MockRequest:
    headers = {"Content-Type": "multipart/form-data"}

    def __init__(self, entity, *args, **kwargs):
        self.files = {f"test_file_{entity}": File(entity)}


class MockEngine:
    def insert(self, entity, data):
        object = ENTITY_MAP[entity](*data)
        return object


class MockApp:
    def __init__(self):
        self.config = {"ENGINE": MockEngine()}


def test_bulk_upload_departments():
    Utils.request = MockRequest("departments")
    Utils.app = MockApp()

    errors = Utils.bulk_upload("departments")

    assert len(errors) == 0

    errors = Utils.bulk_upload("hired_employees")

    assert not os.path.exists("imported/test_file_departments.csv")
    assert len(errors) == 1500


def test_bulk_upload_hired_employees():
    Utils.request = MockRequest("hired_employees")
    Utils.app = MockApp()

    errors = Utils.bulk_upload("hired_employees")

    assert len(errors) == 0

    errors = Utils.bulk_upload("departments")

    assert not os.path.exists("imported/test_file_hired_employees.csv")
    assert len(errors) == 1500


def test_save_as_csv():
    for entity, Class in ENTITY_MAP.items():
        filename = "save_test_file.csv"
        file_path = Utils.save_as_csv(filename, [Class(*MAP[entity]).dict()] * 10)

        assert os.path.exists(file_path)
        os.remove(file_path)

        assert not os.path.exists(file_path)


def test_delete_tmp():
    for entity, Class in ENTITY_MAP.items():
        filename = "save_test_file.csv"
        file_path = Utils.save_as_csv(filename, [Class(*MAP[entity]).dict()] * 10)
        assert os.path.exists(file_path)
        Utils.delete_tmp(file_path)

        assert not os.path.exists(file_path)


def test_delete_tmp_file():
    pass
