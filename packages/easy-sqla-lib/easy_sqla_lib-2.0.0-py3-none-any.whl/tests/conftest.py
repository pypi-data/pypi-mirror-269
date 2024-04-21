from __future__ import annotations

import os.path

import pytest

from easy_sqla.manager import Manager
from tests.base_model import base_model, FILE_PATH

# noinspection PyProtectedMember
base_model.metadata.create_all(base_model.db_context._engine)


def pytest_sessionfinish(session, exitstatus):
    if os.path.exists(FILE_PATH):
        os.remove(FILE_PATH)


@pytest.fixture(scope="class")
def test_context():
    yield Manager.db_context
