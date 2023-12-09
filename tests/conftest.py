import json
import os
import tempfile
from io import BytesIO

import pandas as pd
import pytest

from pushboards import create_app
from pushboards.auth.models import User
from pushboards.extensions import db


@pytest.fixture(scope="session")
def app():
    app = create_app(FORCE_ENV_FOR_DYNACONF="testing")
    with app.app_context():
        db.create_all()
        user = User(email="XXXXXXXXXXXXX")
        user.id = 1
        db.session.add(user)
        db.session.commit()
    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    test_client = app.test_client()
    with test_client.session_transaction() as session:
        session["user_id"] = 1
    return test_client


@pytest.fixture()
def mock_file_source() -> BytesIO:
    json_data = {"col": [1, 2, 3]}
    return BytesIO(json.dumps(json_data).encode("utf-8"))


@pytest.fixture()
def temp_file_path() -> str:
    file_fd, file_path = tempfile.mkstemp()
    os.close(file_fd)
    yield file_path
    os.unlink(file_path)


@pytest.fixture()
def mock_file_data(mock_file_source):
    return pd.read_json(mock_file_source, orient="records")


@pytest.fixture()
def mock_import_fn(mock_file_data):
    def mock_import_fn(data: BytesIO) -> pd.DataFrame:
        return mock_file_data

    return mock_import_fn
