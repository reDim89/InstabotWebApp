#!flask/bin/python
from wtforms import Form, TextField, PasswordField, IntegerField
from wtforms.validators import Required


class LoginForm(Form):
    login = TextField('Login', [Required()])
    password = PasswordField('Password', [Required()])
    like_per_day = IntegerField('Likes per day')
    comments_per_day = IntegerField('Comments per day')
    follow_per_day = IntegerField('Follow per day')


class LogoutForm(Form):
    login = TextField('Login', [Required()])
    password = PasswordField('Password', [Required()])
