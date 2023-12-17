from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, InputRequired, Length

from pushboards.main.models import ImportFunction


class ImportFunctionForm(FlaskForm):
    func_name = StringField(
        "Название",
        validators=[
            DataRequired(message="Название функции - обязательное поле."),
            Length(max=128, message="Слишком длинное название."),
        ],
    )
    func_class = StringField(
        "Python класс",
        validators=[
            DataRequired(message="Python класс - обязательное поле."),
            Length(max=128, message="Слишком длинное название."),
        ],
    )
    func_description = TextAreaField(
        "Описание",
    )
    func_submit = SubmitField("Сохранить")


class ReportForm(FlaskForm):
    report_name = StringField(
        "Название",
        validators=[
            DataRequired(message="Название отчёта - обязательное поле."),
            Length(max=128, message="Слишком длинное название."),
        ],
    )
    report_func = SelectField(
        "Функция импорта",
        validators=[InputRequired(message="Некорректная функция импорта.")],
        coerce=int,
    )
    report_description = TextAreaField("Описание")
    report_submit = SubmitField("Сохранить")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        import_functions = ImportFunction.query.all()
        if import_functions:
            self.report_func.choices = [(func.id, func.func_name) for func in import_functions]
            self.report_func.default = self.report_func.choices[0][0]
