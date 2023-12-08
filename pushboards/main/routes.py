import urllib.parse
from pathlib import Path
from uuid import uuid4

from flask import Blueprint, Response, abort, current_app, jsonify, render_template, request
from flask_login import current_user, login_required

from pushboards.extensions import db
from pushboards.main.models import UserFile
from pushboards.main.upload.process import pandas_pickle_to_excel, pandas_pickle_to_html, process

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

    file_uuid = uuid4().hex
    file_path: Path = (
        Path(current_app.static_folder) / current_app.config.get("static_upload_path") / file_uuid
    ).with_suffix(current_app.config["file_upload_suffix"])
    file_post.stream = process(file_post.stream, current_app.config["CONF_SHEET_NAME"])
    file_post.save(file_path)
    user_file = UserFile(file_name=file_post.filename, file_path=str(file_path), user_id=current_user.id)
    db.session.add(user_file)
    db.session.commit()
    return jsonify({"status": "ok", "file_name": user_file.file_name, "id": user_file.id})


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


@bp.route("/download/<int:file_id>", methods=["GET"])
def download(file_id):
    file = UserFile.query.get_or_404(file_id)
    if file and file.user_id == current_user.id:
        file_path = Path(file.file_path)
        if file_path.exists():
            output_data = pandas_pickle_to_excel(file_path)
            encoded_file_name = urllib.parse.quote(file.file_name)
            return Response(
                output_data,
                mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                headers={"Content-Disposition": f"attachment;filename={encoded_file_name}"},
            )
    abort(404)


@bp.route("/show/<int:file_id>", methods=["GET"])
def show(file_id):
    file = UserFile.query.get_or_404(file_id)
    if file and file.user_id == current_user.id:
        file_path = Path(file.file_path)
        if file_path.exists():
            file_data = pandas_pickle_to_html(file_path)
            return render_template("main/show.html", file=file, file_data=file_data)
    abort(404)
