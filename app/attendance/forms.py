from flask.ext.wtf import Form
from wtforms import SubmitField, FileField, FieldList


class FileUploadForm(Form):
    uploads = FieldList(FileField())
    submit = SubmitField('submit')


