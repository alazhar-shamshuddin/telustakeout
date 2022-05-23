"""
Copyright (c) 2019 - present AppSeed.us
"""

from urllib import request
from xmlrpc.client import Boolean
from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    DateTimeField,
    HiddenField,
    PasswordField,
    SelectMultipleField,
    StringField
)
from wtforms.validators import (
    AnyOf,
    DataRequired,
    Email,
    EqualTo,
    Length
)


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
                        validators=[Length(min=10, max=12)])

    address = StringField('Address', id='address_update')


class CreateOrderForm(FlaskForm):
    username = HiddenField('Username', validators=[DataRequired()])

    email = StringField('Email', validators=[DataRequired(), Email()])

    is_delivery = BooleanField('IsDelivery', validators=[DataRequired()])

    address = StringField('Address')

    phone = StringField('Phone Number', validators=[Length(min=10, max=12)])

    ordered_at = DateTimeField('Ordered At')

    requested_at = DateTimeField('Requested At')

    status = HiddenField('Status', validators=[AnyOf('Ordered')])
