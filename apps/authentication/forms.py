"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, Length


# login and registration

class LoginForm(FlaskForm):
    username = StringField('Username',
                           id='username_login',
                           validators=[DataRequired()])

    password = PasswordField('Password',
                             id='pwd_login',
                             validators=[DataRequired()])


class CreateAccountForm(FlaskForm):
    username = StringField('Username',
                           id='username_create',
                           validators=[DataRequired()])

    email = StringField('Email',
                        id='email_create',
                        validators=[DataRequired(), Email()])

    password = PasswordField('Password',
                             id='pwd_create',
                             validators=[DataRequired()])


class UpdateAccountForm(FlaskForm):
    email = StringField('Email',
                        id='email_update',
                        validators=[DataRequired(), Email()])

    password = PasswordField('Password',
                             id='pwd_update',
                             validators=[DataRequired()])

    full_name = StringField('Full Name', id='full_name_update')

    phone = StringField('Phone Number',
                        id='phone_update',
                        validators=[Length(min=10, max=10)])

    address = StringField('Address', id='address_update')