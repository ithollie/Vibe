
from flask_wtf import Form
from wtforms import StringField, BooleanField,PasswordField
from wtforms.validators import DataRequired
from wtforms import Form, BooleanField, StringField, PasswordField, validators

class RegForm(Form):
        firstname = StringField('firstname', validators=[DataRequired()])
        lastname = StringField('lastnamed', validators=[DataRequired()])
        eamil = StringField('eamil', validators=[DataRequired()])
        password = PasswordField('password', [validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
        ])
        confirm = PasswordField('Repeat Password')
        accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])
        

