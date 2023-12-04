from flask import Blueprint, abort, current_app, redirect, render_template, url_for
from flask_login import current_user, login_user, logout_user

from pushboards.auth.models import User
from pushboards.extensions import db, login_manager

bp = Blueprint("auth", __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@bp.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    return render_template("auth/index.html")


@bp.route("/login/<authenticator>")
def login(authenticator: str):
    oauth_ext = current_app.extensions["authlib.integrations.flask_client"]
    oauth_client = oauth_ext.create_client(authenticator)
    if not oauth_client:
        abort(404)
    redirect_uri = url_for("auth.callback", authenticator=authenticator, _external=True)
    return oauth_client.authorize_redirect(redirect_uri)


@bp.route("/callback/<authenticator>")
def callback(authenticator: str):
    oauth_ext = current_app.extensions["authlib.integrations.flask_client"]
    oauth_client = oauth_ext.create_client(authenticator)
    if not oauth_client:
        abort(404)
    token = oauth_client.authorize_access_token()
    user_info = oauth_client.userinfo(token=token)
    profile = oauth_client.map_profile(user_info)
    if not profile["email"]:
        abort(400)
    user = User.query.filter_by(email=profile["email"]).first()
    if not user:
        user = User(profile["email"])
        db.session.add(user)
    user.full_name = profile["full_name"]
    user.picture = profile["picture"]
    db.session.commit()
    login_user(user)
    return redirect(url_for("main.index"))


@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.index"))
