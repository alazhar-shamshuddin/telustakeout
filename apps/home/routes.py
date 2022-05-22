"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound

from apps import db
from apps.authentication.util import hash_pass
from apps.authentication.forms import UpdateAccountForm
from apps.authentication.models import Users
from pprint import pprint


@blueprint.route('/index')
@login_required
def index():
    return render_template('home/index.html', segment='index')


@blueprint.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    update_account_form = UpdateAccountForm(request.form)

    pprint(request.form)

    if 'profile' in request.form:
        username = current_user.username
        email = request.form['email']

        # Check if another user has the same email address.
        user = Users.query.filter_by(email=email).first()
        if user.username != username:
            return render_template('home/profile.html',
                                   msg='Email already registered to another user',
                                   success=False,
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
                                msg='Profile updated successfully',
                                success=True,
                                user=current_user,
                                form=update_account_form)

    else:
        print('in else')
        return render_template('home/profile.html',
                               user=current_user,
                               form=update_account_form)


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
