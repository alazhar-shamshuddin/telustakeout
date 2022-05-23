"""
Copyright (c) 2019 - present AppSeed.us
"""

from re import L
from urllib import request
from xmlrpc.client import Boolean
from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    DateTimeField,
    HiddenField,
    PasswordField,
    RadioField,
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
    username = StringField('Username')

    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(),
            Length(max=64)
        ])

    full_name = StringField(
        'Full Name',
        validators=[Length(max=64)])

    phone = StringField(
        'Phone Number',
        validators=[Length(max=12)])

    address = StringField(
        'Address',
        validators=[Length(max=255)])

    is_employee = BooleanField('Is Telus TakeOut Employee')

    password = PasswordField(
        'Password',
        validators=[DataRequired()])


class CreateOrderForm(FlaskForm):
    username = HiddenField('Username', validators=[DataRequired()])

    email = StringField('Email', validators=[DataRequired(), Email()])

    is_delivery = BooleanField('IsDelivery', validators=[DataRequired()])

    address = StringField('Address')

    phone = StringField('Phone Number', validators=[Length(min=10, max=12)])

    ordered_at = DateTimeField('Ordered At')

    requested_at = DateTimeField('Requested At')

    status = HiddenField('Status', validators=[AnyOf('Ordered')])
