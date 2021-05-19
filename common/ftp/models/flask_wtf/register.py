#from flask_wtf import Form
from flask_wtf import Form
from flask_wtf.file import FileField, FileAllowed
from wtforms import validators, StringField, PasswordField
from wtforms.fields.html5 import EmailField


class RegisterForm(Form):
    name = StringField('name', [validators.Required()])
    last = StringField( 'last',[validators.Required()])
    email = StringField('email', [validators.Required()])
    password = PasswordField('password', [validators.Required(),validators.EqualTo('confirm', message='Passwords must match'),
            validators.Length(min=4, max=80)
        ])
    confirm = PasswordField('repect password')
    date = StringField('birth', [validators.Required()])
    filename = FileField('image', validators =[validators.Required(),FileAllowed(['jpg', 'png'], 'Images only')])
