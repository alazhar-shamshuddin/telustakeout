from pickletools import UP_TO_NEWLINE
from turtle import up, update
from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound

from apps import db
from apps.authentication.util import hash_pass
from apps.authentication.forms import UpdateAccountForm, CreateOrderForm
from apps.authentication.models import Users, Orders, OrderDetails
from pprint import pprint


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
    create_order_form = CreateOrderForm(request.form)

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

    if 'order' in request.form:
        order = Orders(**request.form)
        db.session.add(order)
        #db.session.commit()

        return render_template('accounts/order.html',
                            msg='Order submitted successfully',
                            success=True,
                            user=current_user,
                            foods=foods,
                            selectedFood=selectedFood,
                            form=create_order_form)

    else:
        return render_template('home/order.html',
                                user=current_user,
                                foods=foods,
                                selectedFood=selectedFood,
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
