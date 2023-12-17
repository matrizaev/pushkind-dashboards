from pushboards.oauth2.yandex import YandexOauth2Config


def test_yandex_oauth2_config_map_profile():
    assert YandexOauth2Config.map_profile(
        {
            "default_email": "email",
            "display_name": "full_name",
            "default_avatar_id": "picture",
            "is_avatar_empty": False,
        }
    ) == {
        "email": "email",
        "full_name": "full_name",
        "picture": "https://avatars.yandex.net/get-yapic/picture/islands-200",
    }
