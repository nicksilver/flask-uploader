from flask_wtf import FlaskForm
from wtforms import SubmitField
from flask_wtf.file import FileField, FileRequired


class UploadForm(FlaskForm):
    file_level = FileField(validators=[FileRequired()])
    file_histyield = FileField(validators=[FileRequired()])
    submit = SubmitField('Submit')
