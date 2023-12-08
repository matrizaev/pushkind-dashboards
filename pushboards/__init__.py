import logging
import sys

from dynaconf import FlaskDynaconf
from flask import Flask, render_template, request

from pushboards import admin, auth, main
from pushboards.extensions import bootstrap, db, login_manager, migrate, oauth_client
from pushboards.oauth2.google import GoogleOauth2Config
from pushboards.oauth2.yandex import YandexOauth2Config


def create_app(**config):
    app = Flask(__name__)
    FlaskDynaconf(app, **config)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    configure_logger(app)

    return app


def register_extensions(app):
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
    login_manager.login_message = "Пожалуйста, авторизуйтесь, чтобы увидеть эту страницу."
    login_manager.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)


def register_blueprints(app):
    app.register_blueprint(admin.routes.bp, url_prefix="/admin")
    app.register_blueprint(auth.routes.bp, url_prefix="/auth")
    app.register_blueprint(main.routes.bp, url_prefix="/")


def register_errorhandlers(app):
    """Register error handlers."""

    def wants_json_response():
        return request.accept_mimetypes["application/json"] >= request.accept_mimetypes["text/html"]

    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, "code", 500)
        if wants_json_response():
            return {"error": error.description}, error_code
        return render_template(f"errors/{error_code}.html", error=error), error_code

    for errcode in [400, 401, 403, 404, 413, 500, 503]:
        app.errorhandler(errcode)(render_error)


def register_shellcontext(app):
    """Register shell context objects."""

    def shell_context():
        """Shell context objects."""
        return {"db": db, "User": auth.models.User, "UserFiles": main.models.UserFile}

    app.shell_context_processor(shell_context)


def configure_logger(app):
    """Configure loggers."""
    handler = logging.StreamHandler(sys.stdout)
    if not app.logger.handlers:
        app.logger.addHandler(handler)
