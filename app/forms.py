#!flask/bin/python
from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, IntegerField, SubmitField
from wtforms.validators import Required


class LoginForm(FlaskForm):
    login = TextField('Login', [Required()])
    password = PasswordField('Password', [Required()])
    like_per_day = IntegerField('Likes per day')
    comments_per_day = IntegerField('Comments per day')
    follow_per_day = IntegerField('Follow per day')
    submit = SubmitField(label='Login and run bot')


class ControlPanelForm(FlaskForm):
    refresh = SubmitField(label='Refresh')
    logout = SubmitField(label='Stop and logout')
