from pathlib import Path
from uuid import uuid4

from flask import Blueprint, abort, current_app, jsonify, render_template, request, url_for
from flask_login import current_user, login_required

from pushboards.extensions import db
from pushboards.main.models import UserFile
from pushboards.main.process import process

bp = Blueprint("main", __name__)


@bp.route("/")
@bp.route("/index/")
@login_required
def index():
    return render_template("main/index.html")


@bp.route("/upload", methods=["POST"])
@login_required
def upload():
    file_post = request.files.get("file")
    if not file_post:
        abort(400)

    file_path: Path = (
        Path(current_app.static_folder) / current_app.config.get("static_upload_path") / uuid4().hex
    ).with_suffix(current_app.config["file_upload_suffix"])
    file_post.stream = process(file_post.stream)
    file_post.save(file_path)
    file_url = url_for("static", filename=file_path.relative_to(current_app.static_folder))
    user_file = UserFile(file_post.filename, str(file_path), file_url, current_user.id)
    db.session.add(user_file)
    db.session.commit()
    return jsonify({"status": "ok", "file_url": file_url, "file_name": user_file.file_name, "id": user_file.id})


@bp.route("/remove/<int:file_id>", methods=["POST"])
@login_required
def remove(file_id):
    file = UserFile.query.get_or_404(file_id)
    if file and file.user_id == current_user.id:
        Path(file.file_path).unlink(missing_ok=True)
        db.session.delete(file)
        db.session.commit()
    else:
        abort(404)
    return jsonify({"status": "ok"})
