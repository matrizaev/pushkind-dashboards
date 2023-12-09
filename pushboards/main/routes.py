import functools
import urllib.parse
from pathlib import Path
from uuid import uuid4

from flask import Blueprint, Response, abort, current_app, jsonify, render_template, request
from flask_login import current_user, login_required

from pushboards.extensions import db
from pushboards.main.models import UserFile
from pushboards.main.upload.excel_processor import process

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

    file_uuid_name = Path(uuid4().hex).with_suffix(current_app.config["file_upload_suffix"])
    file_path: Path = Path(current_app.static_folder) / current_app.config.get("static_upload_path") / file_uuid_name

    import_fn = functools.partial(process, conf_sheet_name=current_app.config["CONF_SHEET_NAME"])

    user_file = UserFile(
        file_name=file_post.filename,
        file_path=file_path,
        user_id=current_user.id,
        file_data=file_post.stream,
        import_fn=import_fn,
    )

    db.session.add(user_file)
    db.session.commit()
    return jsonify({"status": "ok", "file_name": user_file.file_name, "id": user_file.id})


@bp.route("/remove/<int:file_id>", methods=["POST"])
@login_required
def remove(file_id: int):
    file = UserFile.query.get_or_404(file_id)
    if file and file.user_id == current_user.id:
        file.remove_data()
        db.session.delete(file)
        db.session.commit()
        return jsonify({"status": "ok"})
    abort(404)


@bp.route("/download/<int:file_id>", methods=["GET"])
def download(file_id: int):
    file = UserFile.query.get_or_404(file_id)
    if file and file.user_id == current_user.id:
        if file.file_path.exists():
            output_data = file.to_excel()
            encoded_file_name = urllib.parse.quote(file.file_name)
            return Response(
                output_data,
                mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                headers={"Content-Disposition": f"attachment;filename={encoded_file_name}"},
            )
    abort(404)


@bp.route("/show/<int:file_id>", methods=["GET"])
def show(file_id: int):
    file = UserFile.query.get_or_404(file_id)
    if file and file.user_id == current_user.id:
        if file.file_path.exists():
            file_data = file.to_html()
            return render_template("main/show.html", file=file, file_data=file_data)
    abort(404)
