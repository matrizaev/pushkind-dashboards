from pushboards.auth.models import User


def test_user():
    user = User(email="XXXXXXXXXXXXX")
    user.id = 1
    user.full_name = "1"
    user.picture = "2"

    assert user.to_json() == {"id": 1, "email": "xxxxxxxxxxxxx", "full_name": "1", "picture": "2", "files": []}
