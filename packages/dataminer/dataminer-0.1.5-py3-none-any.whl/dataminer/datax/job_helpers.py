import json


class JobBuilder:
    def __init__(self):
        self.job = {"job": {"setting": {"speed": {"channel": 1}}, "content": [{}]}}

    def add_reader(self, reader: dict):
        self.job["job"]["content"][0]["reader"] = reader
        return self

    def add_writer(self, writer: dict):
        self.job["job"]["content"][0]["writer"] = writer
        return self

    def build(self):
        return self.job

    @staticmethod
    def save_job(datax_job: dict, file_path: str = "datax_job.json"):
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(datax_job, f, indent=4, ensure_ascii=False)


class RDBMSReaderBuilder:
    def __init__(self):
        self.cfg = {
            "name": "rdbmsreader",
            "parameter": {
                "username": "",
                "password": "",
                "connection": [{"jdbcUrl": [""], "querySql": [""]}],
                "fetchSize": 10000,
            },
        }

    def set_username(self, username: str):
        self.cfg["parameter"]["username"] = username
        return self

    def set_password(self, password: str):
        self.cfg["parameter"]["password"] = password
        return self

    def set_query_sql(self, sql: str):
        self.cfg["parameter"]["connection"][0]["querySql"] = [sql]
        return self

    def set_jdbc_url(self, jdbcUrl: str):
        self.cfg["parameter"]["connection"][0]["jdbcUrl"] = [jdbcUrl]
        return self

    def set_fetch_size(self, fetch_size: int = 10000):
        self.cfg["parameter"]["fetchSize"] = fetch_size
        return self

    def build(self):
        return self.cfg


class RDBMSWriterBuilder:
    def __init__(self):
        self.cfg = {
            "name": "rdbmswriter",
            "parameter": {
                "username": "",
                "password": "",
                "connection": [{"jdbcUrl": "", "table": [""]}],
                "preSql": [""],
                "column": [""],
            },
        }

    def set_username(self, username: str):
        self.cfg["parameter"]["username"] = username
        return self

    def set_password(self, password: str):
        self.cfg["parameter"]["password"] = password
        return self

    def set_table(self, table: str):
        self.cfg["parameter"]["connection"][0]["table"] = [table]
        return self

    def set_jdbc_url(self, jdbcUrl: str):
        self.cfg["parameter"]["connection"][0]["jdbcUrl"] = jdbcUrl
        return self

    def set_pre_sql(self, presql: str):
        self.cfg["parameter"]["preSql"] = [presql]
        return self

    def set_columns(self, columns: list[str]):
        self.cfg["parameter"]["column"] = columns
        return self

    def build(self):
        return self.cfg


class DorisWriterBuilder:
    def __init__(self):
        self.cfg = {
            "name": "doriswriter",
            "parameter": {
                "loadUrl": [],
                "username": "",
                "password": "",
                "connection": [{"jdbcUrl": "", "selectedDatabase": "", "table": [""]}],
                "column": [""],
                "loadProps": {
                    "format": "json",
                    "strip_outer_array": True,
                },
            },
        }

    def set_load_url(self, load_url: list[str]):
        self.cfg["parameter"]["loadUrl"] = load_url
        return self

    def set_username(self, username: str):
        self.cfg["parameter"]["username"] = username
        return self

    def set_password(self, password: str):
        self.cfg["parameter"]["password"] = password
        return self

    def set_selected_database(self, database: str):
        self.cfg["parameter"]["connection"][0]["selectedDatabase"] = database
        return self

    def set_table(self, table: str):
        self.cfg["parameter"]["connection"][0]["table"] = [table]
        return self

    def set_jdbc_url(self, jdbc_url: str):
        self.cfg["parameter"]["connection"][0]["jdbcUrl"] = jdbc_url
        return self

    def set_presql(self, presql: str):
        self.cfg["parameter"]["presql"] = [presql]
        return self

    def set_columns(self, columns: list[str]):
        self.cfg["parameter"]["column"] = columns
        return self

    def build(self):
        return self.cfg
