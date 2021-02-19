from flask_wtf import Form
from wtforms import validators, StringField, PasswordField
from wtforms.fields.html5 import EmailField

class LoginForm(Form):
    email = StringField('t', [validators.Required()])
    password = PasswordField('Password', [validators.Required(),validators.Length(min=4, max=80)
        ])
