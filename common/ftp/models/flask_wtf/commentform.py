from flask_wtf import Form
from wtforms import validators, StringField, PasswordField,TextAreaField
from wtforms.fields.html5 import EmailField

class CommentForm(Form):
    title  = StringField('title', [validators.Required()])
    comment = TextAreaField('comment',[ validators.Required()])
