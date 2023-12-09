from pushboards.main.models import UserFile


def test_userfile(temp_file_path, mock_import_fn, mock_file_source, mock_file_data):
    user_file = UserFile(
        file_name="file_name",
        file_path=temp_file_path,
        user_id=1,
        file_data=mock_file_source,
        import_fn=mock_import_fn,
    )
    user_file.id = 1
    assert user_file.to_json() == {
        "id": 1,
        "file_name": "file_name",
        "file_path": temp_file_path,
        "user_id": 1,
    }

    assert user_file.to_html() == mock_file_data.to_html(
        index=False, header=False, justify="left", classes=["table", "table-striped"]
    )
