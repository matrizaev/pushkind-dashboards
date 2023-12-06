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
