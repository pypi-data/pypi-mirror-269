from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import Field
from pydantic.v1 import BaseSettings, PyObject


class DriverEnum(str, Enum):
    SQLITE = "sqlite"
    MYSQL = "mysql"
    POSTGRES = "postgresql"


class DBSettings(BaseSettings):
    driver: DriverEnum
    host: str = ""
    port: str = ""
    name: str = ""
    username: str = ""
    password: str = ""
    auto_commit: bool = True
    is_test: bool = False
    echo: bool = False
    sqlite_db_path: str = "./tests/db.sqlite3"
    error_handler: Optional[PyObject] = None


    class Config:
        env_prefix = "DB_"
        case_sensitive = False
        allow_mutation = False
