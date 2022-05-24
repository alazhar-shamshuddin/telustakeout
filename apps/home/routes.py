from pprint import pprint
from datetime import datetime, timedelta
from venv import create

from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound

from apps import db
from apps.authentication.util import hash_pass
from apps.authentication.forms import UpdateAccountForm, CreateOrderForm
from apps.authentication.models import Users, Orders, OrderDetails


@blueprint.route('/index')
@login_required
def index():
    return render_template('home/index.html', segment='index')


@blueprint.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'GET':
        update_account_form = UpdateAccountForm(
            username=current_user.username,
            email=current_user.email,
            full_name=current_user.full_name,
            phone=current_user.phone,
            address=current_user.address,
            is_employee=current_user.is_employee
        )
        return render_template('home/profile.html',
                               form=update_account_form)

    else:
        update_account_form = UpdateAccountForm(
            request.form,
            username=current_user.username)

        if update_account_form.validate_on_submit():
            username = current_user.username
            email = request.form['email']

            # Check if another user has the same email address.
            user = Users.query.filter_by(email=email).first()
            if user and (user.username != username):
                message = (
                    'This address is registered to another user; '
                    'please use another email address.')

                update_account_form.email.errors.append(message)

                return render_template('home/profile.html',
                                       success=False,
                                       message=message,
                                       form=update_account_form)

            # Otherwise we can update the user's account info.
            current_user.email = request.form['email']
            current_user.full_name = request.form['full_name']
            current_user.phone = request.form['phone']
            current_user.address = request.form['address']
            current_user.password = hash_pass(request.form['password'])
            db.session.add(current_user)
            db.session.commit()

            return render_template('home/profile.html',
                                    success=True,
                                    form=update_account_form)

        else:
            return render_template('home/profile.html',
                                   success=False,
                                   message='Error',
                                   form=update_account_form)


@blueprint.route('/order', methods=['GET', 'POST'])
@login_required
def order():
    foods = {
        'Pizza': {
            'toppings': ['Black Olives', 'Mushrooms', 'Pepperoni', 'Pineapples'],
        },
        'Sandwich': {
            'toppings': ['Black Olives', 'Lettuce', 'Pineapples', 'Tomatoes'],
        },
    }

    # Process query parameters for pre-selected food to order
    # (e.g.: /orders?food=pizza).  If a food item was specified,
    # ensure it exists in our inventory of valid foods; otherwise
    # set it to none.
    selectedFood = request.args.get('food')
    if selectedFood:
        selectedFood = selectedFood.lower()

        if selectedFood not in [x.lower() for x in foods.keys()]:
            selectedFood = None

    if request.method == 'GET':
        create_order_form = CreateOrderForm(
            username=current_user.username,
            email=current_user.email,
            phone=current_user.phone,
            address=current_user.address,
            requested_at=datetime.now() + timedelta(hours=1),
            item=selectedFood,
        )

        # Create pizza topping titles that lower cased and with no spaces.
        create_order_form.pizza_toppings.choices = \
            generate_choice_tuples(foods['Pizza']['toppings'])

        # Create sandwich topping titles that lower cased and with no spaces.
        create_order_form.sandwich_toppings.choices = \
            generate_choice_tuples(foods['Sandwich']['toppings'])

        return render_template('home/order.html',
                               form=create_order_form)

    else:
        create_order_form = CreateOrderForm(request.form)
        create_order_form.pizza_toppings.choices = \
            generate_choice_tuples(foods['Pizza']['toppings'])
        create_order_form.sandwich_toppings.choices = \
            generate_choice_tuples(foods['Sandwich']['toppings'])

        if create_order_form.validate_on_submit():
            custom_errors = False

            if not create_order_form.delivery_pickup.data:
                # The DataRequired validator for RadioFields doesn't work so
                # this our temporary work around.
                custom_errors = True
                create_order_form.delivery_pickup.errors.append(
                    'This field is required')

            if create_order_form.delivery_pickup.data == 'delivery' and \
               not create_order_form.address.data:
               custom_errors = True
               create_order_form.address.errors.append(
                   'An address is required if you want us to deliver your order.')

            if custom_errors:
                return render_template('home/order.html',
                                        success=False,
                                        message='Error',
                                        form=create_order_form)
            else:
                # There are no errors; save the order.
                create_order_form.ordered_at.data = datetime.now()
                create_order_form.status.data = 'ordered'
                save_order(create_order_form)
                return render_template('home/order.html',
                                       success=True,
                                       form=create_order_form)

        else:
            return render_template('home/order.html',
                                    success=False,
                                    message='Error',
                                    form=create_order_form)


@blueprint.route('/<template>')
@login_required
def route_template(template):
    try:
        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except Exception as e:
        print('in home/routes.py')
        print(e)
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):
    try:
        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None


# Helper to generate topping choices for the orders form
def generate_choice_tuples(toppings):
    titles = [x.lower() for x in toppings]
    titles = [x.replace(' ', '_') for x in titles]
    return [(titles[i], toppings[i]) for i in range(0, len(toppings))]


# Help to save the order to disk.
def save_order(order_form):
    pprint(order_form.data)
    print(order_form.username.data)

    order_header = Orders(
        username=order_form.username.data,
        email=order_form.email.data,
        is_delivery=False,
        address=order_form.address.data,
        phone=order_form.phone.data,
        ordered_at=True,
        requested_at=True,
        status=order_form.status.data)
    db.session.add(order_header)
    db.session.commit()
