from __future__ import annotations

from typing import Dict
from typing import Union

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from easy_sqla.db.settings import DBSettings
from easy_sqla.db.settings import DriverEnum
from easy_sqla.logger import logger as logging


class DBContextMeta(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__call__(*args, **kwargs)

        return cls._instance


class DBContext(metaclass=DBContextMeta):
    def __init__(self, settings: DBSettings):
        self._engine = None
        self._session: Union[Session, None] = None
        self._settings: Dict = settings.dict()
        self.setup_engine()

    def setup_engine(self) -> Union[Engine, None]:
        if not self._settings:
            raise ValueError("Cannot setup engine without settings")

        driver = self._settings.get("driver").value

        try:
            logging.info("Setting up new engine")
            if driver in [DriverEnum.MYSQL, DriverEnum.POSTGRES]:
                engine_ = create_engine(
                    f"{driver}://{self._settings.get('username')}:{self._settings.get('password')}@{self._settings.get('host')}"
                    f":{self._settings.get('port')}/{self._settings.get('name')}",
                    echo=self._settings.get("echo", False),
                    future=True,
                    pool_size=self._settings.get("DB_MAX_POOL", 10),
                    pool_pre_ping=True,
                )

            else:
                engine_ = create_engine(
                    f"{driver}:///{':memory:' if self._settings.get('is_test') else self._settings.get('sqlite_db_path')}"
                )
            engine_.connect()
            self._engine = engine_
            return engine_
        except sqlalchemy.exc.OperationalError as e:
            logging.error(
                "An error occurred while setting up connection to the database. Take a look on traceback",
            )
            logging.error(str(e))
            raise e

    @property
    def settings(self) -> Dict:
        return self._settings

    @property
    def session(self):
        if not self._session:
            session_ = Session(bind=self.setup_engine())
            self._session = session_

        return self._session

    @session.setter
    def session(self, session):
        self._session = session

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            logging.error(
                "An error occurred while doing database operation. Rolling back...",
            )
            logging.exception(exc_tb)
            self.session.rollback()

        else:
            if self.settings.get("auto_commit"):
                self.session.commit()
            else:
                logging.info("Auto commit is disabled. Skipping commit operation")
