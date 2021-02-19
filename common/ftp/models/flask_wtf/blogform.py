from flask_wtf import Form
from wtforms import validators, StringField, PasswordField,TextAreaField
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields.html5 import EmailField

class BlogForm(Form):
    author = StringField('author', [validators.Required()])
    title  = StringField('title', [validators.Required()])
    email =  StringField('email', [validators.Required()])
    description = TextAreaField('description',[ validators.Required(),validators.length(max=1100)])
    filename = FileField('image', validators =[validators.Required(),FileAllowed(['jpg', 'png'], 'Images only')])
