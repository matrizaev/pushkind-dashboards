from pushboards.main.models import UserFile


def test_userfile():
    user_file = UserFile("file_name", "file_path", "file_url", 1)
    user_file.id = 1
    assert user_file.to_json() == {
        "id": 1,
        "file_name": "file_name",
        "file_path": "file_path",
        "file_url": "file_url",
        "user_id": 1,
    }
