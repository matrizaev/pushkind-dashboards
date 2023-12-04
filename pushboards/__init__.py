from authlib.integrations.flask_client import OAuth
from dynaconf import FlaskDynaconf
from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from pushboards.oauth2.google import GoogleOauth2Config
from pushboards.oauth2.yandex import YandexOauth2Config

oauth_client = OAuth()
oauth_client.register(
    name=GoogleOauth2Config.NAME,
    client_cls=GoogleOauth2Config,
)
oauth_client.register(
    name=YandexOauth2Config.NAME,
    client_cls=YandexOauth2Config,
)

login_manager = LoginManager()
login_manager.login_view = "auth.index"

migrate = Migrate()

db = SQLAlchemy()

bootstrap = Bootstrap5()


def create_app():
    app = Flask(__name__)
    FlaskDynaconf(app)

    oauth_client.init_app(app)

    login_manager.init_app(app)

    db.init_app(app)

    migrate.init_app(app, db)

    bootstrap.init_app(app)

    from pushboards.admin.routes import bp as admin_bp  # noqa: C0415
    from pushboards.auth.routes import bp as auth_bp  # noqa: C0415
    from pushboards.main.routes import bp as main_bp  # noqa: C0415

    app.register_blueprint(admin_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(main_bp)

    return app


# from pushboards.auth import models as auth_models  # noqa: E402,F401
# from pushboards.main import models as main_models  # noqa: E402,F401
