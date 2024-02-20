from api.models import (
    Base,
    Department,
    HiredEmployee,
    Job
)
from sqlalchemy import create_engine, text


ENTITY_MAP = {
    "departments": Department,
    "hired_employees": HiredEmployee,
    "jobs": Job
}


class Engine:
    base = Base()

    def __init__(self):
        self.engine = create_engine("sqlite:///globant_code_challenge.db", echo=True)
        self.base.metadata.create_all(bind=self.engine)

    def query(self, query):
        with self.engine.connect() as conn:
            results = conn.execute(text(query))
            return [list(r) for r in results]
            
    def insert(self, entity, raw_data):
        data_object = ENTITY_MAP[entity](*raw_data)
        print(data_object)
        table = self.base.metadata.tables[entity]

        try:
            print(table.columns)
            statement = table.insert().values(**data_object.dict())
            print("\nStatement\n", statement)
            statement = statement.compile()
        except Exception as e:
            print(e)
            raise Exception(e)

        with self.engine.connect() as conn:
            conn.execute(statement)
            conn.commit()
        print(data_object)
    

    def all(self, entity):
        table = self.base.metadata.tables[entity]
        with self.engine.connect() as conn:
            query = table.select()

            print("Query", query)
            query = query.compile()
            print("Query", query)

            results = conn.execute(query)

            selected_results = [ENTITY_MAP[entity](*result).dict() for result in results]

            return {
                entity: selected_results
            }
