from pathlib import Path

from flask import Blueprint, abort, jsonify, render_template, request
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
    file_post = request.files["file"]
    user_file = UserFile(file_post=file_post, user_id=current_user.id, process_fn=process)
    db.session.add(user_file)
    db.session.commit()
    return jsonify(
        {"status": "ok", "file_url": user_file.file_url, "file_name": user_file.file_name, "id": user_file.id}
    )


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
