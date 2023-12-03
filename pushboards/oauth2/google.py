from authlib.integrations.flask_client.apps import FlaskOAuth2App


class GoogleOauth2Config(FlaskOAuth2App):
    NAME = "google"
    OAUTH_APP_CONFIG = {
        "api_base_url": "https://www.googleapis.com/",
        "server_metadata_url": "https://accounts.google.com/.well-known/openid-configuration",
        "client_kwargs": {"scope": "openid email profile"},
        "userinfo_endpoint": "https://openidconnect.googleapis.com/v1/userinfo",
    }

    @staticmethod
    def map_profile(user_info: dict) -> dict:
        return {
            "email": user_info.get("email"),
            "full_name": user_info.get("name"),
            "picture": user_info.get("picture"),
        }
