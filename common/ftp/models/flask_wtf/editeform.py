from flask_wtf import Form
from wtforms import validators, StringField, PasswordField,TextAreaField
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields.html5 import EmailField

class EditeForm(Form):
        description = TextAreaField('description',[ validators.Required(),validators.length(max=1100)])
