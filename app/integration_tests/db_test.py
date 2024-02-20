from ..api.db_engine import Engine
import os
import logging

logging.getLogger('sqlalchemy.engine.Engine').disabled = True

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

engine: Engine = None


def integration_test_metadata_created():
    assert engine.base.metadata.tables
    table_keys = engine.base.metadata.tables.keys()
    assert "hired_employees" in table_keys
    assert "departments" in table_keys
    assert "jobs" in table_keys


def integration_test_remove_db():
    os.remove("test_db.db")


def setup():
    return Engine(db="test_db.db")


if __name__ == '__main__':
    engine = setup()
    functions =  [f for f in filter(callable, locals().values()) if "integration_test_" in f.__name__]
    for function in functions:
        try:
            function()
            print(f"{function.__name__}... PASSED")
        except Exception as e:
            print(f"{function.__name__}... FAILED\n", e)
    