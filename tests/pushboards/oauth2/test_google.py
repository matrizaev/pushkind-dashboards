from pushboards.oauth2.google import GoogleOauth2Config


def test_google_oauth2_config_map_profile():
    assert GoogleOauth2Config.map_profile(
        {
            "email": "email",
            "name": "full_name",
            "picture": "picture",
        }
    ) == {
        "email": "email",
        "full_name": "full_name",
        "picture": "picture",
    }
