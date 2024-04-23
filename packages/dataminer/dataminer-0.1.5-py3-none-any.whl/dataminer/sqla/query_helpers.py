from sqlalchemy import Engine, Select


class QueryHelper:

    def __init__(self, engine: Engine):
        self.engine = engine

    def get_sql(self, select: Select) -> str:
        return str(
            select.compile(
                dialect=self.engine.dialect, compile_kwargs={"literal_binds": True}
            )
        )
