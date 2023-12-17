from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required
from sqlalchemy.exc import IntegrityError

from pushboards.admin.forms import ImportFunctionForm, ReportForm
from pushboards.auth.models import User
from pushboards.extensions import db
from pushboards.main.models import ImportFunction, Report

bp = Blueprint("admin", __name__)


@bp.route("/")
@login_required
def index():
    users = User.query.all()
    funcs = ImportFunction.query.all()
    reports = Report.query.all()
    forms = {
        "import_function": ImportFunctionForm(),
        "report": ReportForm(),
    }
    return render_template("admin/index.html", users=users, funcs=funcs, reports=reports, forms=forms)


@bp.route("/report/", methods=["POST"])
@login_required
def add_report():
    form = ReportForm()
    if form.validate_on_submit():
        func = ImportFunction.query.get_or_404(form.report_func.data)
        report = Report(report_name=form.report_name.data, description=form.report_description.data, func=func)
        db.session.add(report)
        db.session.commit()
        flash("Отчет добавлен.")
    else:
        for message in form.errors.values():
            flash(message, "danger")
    return redirect(url_for("admin.index"))


@bp.route("/report/<int:report_id>", methods=["POST"])
@login_required
def modify_report(report_id: int):
    report = Report.query.get_or_404(report_id)
    form = ReportForm()
    if form.validate_on_submit():
        func = ImportFunction.query.get_or_404(form.report_func.data)
        report.report_name = form.report_name.data
        report.description = form.report_description.data
        report.func = func
        db.session.commit()
        flash("Отчет изменен.")
    else:
        for message in form.errors.values():
            flash(message, "danger")
    return redirect(url_for("admin.index"))


@bp.route("/function/", methods=["POST"])
@login_required
def add_function():
    form = ImportFunctionForm()
    if form.validate_on_submit():
        try:
            import_function = ImportFunction(
                func_name=form.func_name.data, description=form.func_description.data, func_class=form.func_class.data
            )
        except AttributeError:
            flash("Неверный класс функции.", "danger")
            return redirect(url_for("admin.index"))
        db.session.add(import_function)
        try:
            db.session.commit()
            flash("Функция добавлена.")
        except IntegrityError:
            db.session.rollback()
            flash("Функция с таким классом уже существует.", "danger")
    else:
        for message in form.errors.values():
            flash(message, "danger")
    return redirect(url_for("admin.index"))


@bp.route("/function/<int:func_id>", methods=["POST"])
@login_required
def modify_function(func_id: int):
    import_function = ImportFunction.query.get_or_404(func_id)
    form = ImportFunctionForm()
    if form.validate_on_submit():
        import_function.func_name = form.func_name.data
        import_function.description = form.func_description.data
        try:
            import_function.attach_func_class(form.func_class.data)
        except AttributeError:
            flash("Неверный класс функции.", "danger")
            return redirect(url_for("admin.index"))
        try:
            db.session.commit()
            flash("Функция добавлена.")
        except IntegrityError:
            db.session.rollback()
            flash("Функция с таким классом уже существует.", "danger")
    else:
        for message in form.errors.values():
            flash(message, "danger")
    return redirect(url_for("admin.index"))
