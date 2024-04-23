import datetime
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path


def filter_none(value: dict):
    if isinstance(value, dict):
        return {k: filter_none(v) for k, v in value.items() if v is not None}
    elif isinstance(value, list):
        return [filter_none(v) for v in value]
    else:
        return value


class DataxRunner:
    def __init__(self, datax_home: str) -> None:
        self.datax_path = "/".join((str(datax_home), "bin/datax.py"))

    def resolve_result(self, datax_result: dict) -> dict:
        date_format = "%Y-%m-%d %H:%M:%S"

        std_out = datax_result["stdout"]

        for line in std_out.splitlines():
            if re.compile(r"任务启动时刻").match(line):
                line_list = line.split(":", 1)
                line_list = [r.strip() for r in line_list]
                datax_result["start_time"] = datetime.datetime.strptime(
                    line_list[1], date_format
                )
            if re.compile(r"任务结束时刻").match(line):
                line_list = line.split(":", 1)
                line_list = [r.strip() for r in line_list]
                datax_result["end_time"] = datetime.datetime.strptime(
                    line_list[1], date_format
                )
            if re.compile(r"任务总计耗时").match(line):
                line_list = line.split(":", 1)
                line_list = [r.strip() for r in line_list]
                datax_result["seconds"] = line_list[1]
            if re.compile(r"任务平均流量").match(line):
                line_list = line.split(":", 1)
                line_list = [r.strip() for r in line_list]
                datax_result["traffic"] = line_list[1]
            if re.compile(r"记录写入速度").match(line):
                line_list = line.split(":", 1)
                line_list = [r.strip() for r in line_list]
                datax_result["write_speed"] = line_list[1]
            if re.compile(r"读出记录总数").match(line):
                line_list = line.split(":", 1)
                line_list = [r.strip() for r in line_list]
                datax_result["read_records"] = line_list[1]
            if re.compile(r"读写失败总数").match(line):
                line_list = line.split(":", 1)
                line_list = [r.strip() for r in line_list]
                datax_result["failed_records"] = line_list[1]

        return datax_result

    def run(self, datax_job: dict) -> dict:

        job = filter_none(datax_job)

        try:
            Path(self.datax_path)
        except Exception as e:
            raise ValueError(f"Invalid path: {self.datax_path}") from e

        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", suffix=".json"
        ) as tf:
            job_file = Path(tf.name).resolve()
            tf.seek(0)
            json.dump(job, tf, indent=4, ensure_ascii=False)
            tf.flush()
            tf.seek(0)

            cmd = f"{sys.executable} {self.datax_path} {job_file}"

            try:
                result = subprocess.run(
                    cmd,
                    shell=True,
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    encoding="utf-8",
                )
            except subprocess.CalledProcessError as e:
                datax_result = {
                    "args": e.args[1],
                    "returncode": e.returncode,
                    "stdout": e.stdout,
                    "stderr": e.stderr,
                }
                return datax_result

            datax_result = {
                "args": result.args,
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
            }

        return self.resolve_result(datax_result)
