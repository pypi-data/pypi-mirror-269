from dataclasses import dataclass
from typing import Optional

from sqlalchemy import Engine, MetaData, Table


@dataclass
class MetaColumn:
    name: str
    type: str
    length: Optional[int] = None
    comment: Optional[str] = None


@dataclass
class MetaTable:
    name: str
    columns: list[MetaColumn]
    comment: Optional[str] = None


class TableInspector:
    def __init__(self, engine: Engine, table: str, schema: str = None):
        self.engine = engine
        self.meta = MetaData(schema=schema) if schema else MetaData()
        self.table = Table(table, self.meta, autoload_with=self.engine)

    def get_comment(self):
        return self.table.comment

    def get_columns(self) -> list[MetaColumn]:
        result = []
        for column in self.table.columns:
            if hasattr(column.type, "length"):
                result.append(
                    MetaColumn(
                        name=column.name,
                        type=column.type.python_type.__name__,
                        length=column.type.length,
                        comment=column.comment,
                    )
                )
            else:
                result.append(
                    MetaColumn(
                        name=column.name,
                        type=column.type.python_type.__name__,
                        comment=column.comment,
                    )
                )
        return result

    def get_meta_table(self) -> MetaTable:
        return MetaTable(
            name=self.table.name,
            columns=self.get_columns(),
            comment=self.get_comment(),
        )
