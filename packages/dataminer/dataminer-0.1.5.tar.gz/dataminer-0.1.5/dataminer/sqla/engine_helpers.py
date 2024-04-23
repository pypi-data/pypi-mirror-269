import re
from dataclasses import dataclass

import oracledb
from sqlalchemy import Engine, NullPool, create_engine


@dataclass
class EngineConfig:
    drivername: str
    host: str
    database: str
    username: str
    password: str
    port: int


class EngineFactory:

    @staticmethod
    def create_engine(cfg: EngineConfig) -> Engine:
        _driver = cfg.drivername
        _username = cfg.username
        url = f"{cfg.drivername}://{cfg.username}:{cfg.password}@{cfg.host}:{cfg.port}/{cfg.database}"

        if re.search(r"oracle", _driver, re.IGNORECASE) and (
            _username.lower() == "sys" or _username.lower() == "system"
        ):
            return create_engine(
                url,
                poolclass=NullPool,
                connect_args={"mode": oracledb.SYSDBA},
            )
        else:
            return create_engine(url, poolclass=NullPool)

    @staticmethod
    def jdbc_from_engine(engine: Engine) -> str:
        dialect = engine.dialect.name
        _host = engine.url.host
        _port = engine.url.port
        _database = engine.url.database
        match dialect:
            case "oracle":
                return f"jdbc:oracle:thin:@{_host}:{_port}/{_database}"
            case "postgresql":
                return f"jdbc:postgresql://{_host}:{_port}/{_database}"
            case "mssql":
                return f"jdbc:sqlserver://{_host}:{_port};databaseName={_database}"
            case "mysql":
                return f"jdbc:mysql://{_host}:{_port}/{_database}"
            case _:
                raise Exception(f"Unsupported dialect: {dialect}")
