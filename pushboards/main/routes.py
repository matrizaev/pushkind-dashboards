from pathlib import Path
from uuid import uuid4

from flask import Blueprint, abort, current_app, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from pushboards import db
from pushboards.main.models import UserFile
from pushboards.main.process import process

bp = Blueprint("main", __name__)


def wants_json_response():
    return request.accept_mimetypes["application/json"] >= request.accept_mimetypes["text/html"]


@bp.route("/")
@bp.route("/index/")
@login_required
def index():
    return render_template("main/index.html")


@bp.route("/upload", methods=["POST"])
@login_required
def upload():
    file_post = request.files["file"]
    file_name = (Path(current_app.config["STATIC_UPLOAD_PATH"]) / f"{uuid4().hex}").with_suffix(".xlsx")
    file_path = Path(current_app.static_folder) / file_name
    file_url = url_for("static", filename=file_name)
    file_data = process(file_post.stream)
    file_path.write_bytes(file_data)
    file = UserFile(file_name=file_post.filename, file_url=file_url, file_path=str(file_path), user=current_user)
    db.session.add(file)
    db.session.commit()
    return jsonify({"status": "ok", "file_url": file_url, "file_name": file_post.filename, "id": file.id})


@bp.route("/remove/<int:file_id>", methods=["POST"])
@login_required
def remove(file_id):
    file = UserFile.query.get_or_404(file_id)
    if file and file.user_id == current_user.id:
        Path(file.file_path).unlink(missing_ok=True)
        db.session.delete(file)
        db.session.commit()
        flash("Файл удален", "success")
    else:
        abort(404)
    if not wants_json_response():
        return redirect(url_for("main.index"))

    return jsonify({"status": "ok"})
