from flask import Flask

from pushboards.admin.routes import bp as admin_bp
from pushboards.auth.routes import bp as auth_bp
from pushboards.extensions import bootstrap, config, db, login_manager, migrate, oauth_client
from pushboards.main.routes import bp as main_bp
from pushboards.oauth2.google import GoogleOauth2Config
from pushboards.oauth2.yandex import YandexOauth2Config


def create_app():
    app = Flask(__name__)
    register_extensions(app)
    register_blueprints(app)

    return app


def register_extensions(app):
    config.init_app(app)
    oauth_client.register(
        name=GoogleOauth2Config.NAME,
        client_cls=GoogleOauth2Config,
    )
    oauth_client.register(
        name=YandexOauth2Config.NAME,
        client_cls=YandexOauth2Config,
    )
    oauth_client.init_app(app)
    login_manager.login_view = "auth.index"
    login_manager.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)


def register_blueprints(app):
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(main_bp, url_prefix="/")


# from pushboards.auth import models as auth_models  # noqa: E402,F401
# from pushboards.main import models as main_models  # noqa: E402,F401
