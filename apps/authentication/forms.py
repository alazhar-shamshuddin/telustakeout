from re import L
from urllib import request
from xmlrpc.client import Boolean
from flask_wtf import FlaskForm
from wtforms import (
    widgets,
    BooleanField,
    DateTimeLocalField,
    PasswordField,
    RadioField,
    SelectMultipleField,
    StringField
)
from wtforms.validators import (
    DataRequired,
    Email,
    Length
)

class MultiCheckboxField(SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.

    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    """
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


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
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=64)])
    delivery_pickup = RadioField(
        'Delivery or Pickup',
        choices=[('delivery','Delivery'), ('pickup','Pickup')],
        default=None,
        validators=[DataRequired()])
    address = StringField('Address', validators=[Length(max=255)])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(max=12)])
    requested_at = DateTimeLocalField(
        'Requested At',
        format='%Y-%m-%dT%H:%M',
        validators=[DataRequired()])
    item = RadioField(
        'Pizza or Sandwich',
        choices=[('pizza','Pizza'), ('sandwich','Sandwich')],
        default=None,
        validators=[DataRequired()])
    pizza_toppings = MultiCheckboxField('Pizza Toppings')
    sandwich_toppings = MultiCheckboxField('Sandwich Toppings')

    # username = HiddenField('Username', validators=[DataRequired()])
    # ordered_at = HiddenField('Ordered At')
    # status = HiddenField('Status')


class CreateOrderDetailsForm(FlaskForm):
    #order_id = HiddenField('order_id', validators=[DataRequired()])
    item = RadioField(
        'Pizza or Sandwich',
        choices=[('pizza','Pizza'), ('sandwich','Sandwich')],
        default=None,
        validators=[DataRequired()])
    toppings = RadioField(
        'Label',
        choices=[(1,'description'), (2,'whatever')],
        default=1,
        coerce=int,
        validators=[DataRequired()])
