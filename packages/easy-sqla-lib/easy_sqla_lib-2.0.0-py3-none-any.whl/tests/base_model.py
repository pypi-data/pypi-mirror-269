from __future__ import annotations

import os

from easy_sqla.db.settings import DBSettings
from easy_sqla.db.settings import DriverEnum
from easy_sqla.manager import Manager

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
FILE_PATH = os.path.join(BASE_DIR, "tests", "sqlite.db")

test_settings = DBSettings(
    driver=DriverEnum.SQLITE,
    sqlite_db_path=FILE_PATH,
)

base_model = Manager.as_base_model(test_settings)
