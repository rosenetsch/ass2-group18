from flask import Blueprint, flash, render_template, request, url_for, redirect
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user
from sqlalchemy import or_
from .models import User
from .forms import LoginForm, RegisterForm
from . import db

# Create a blueprint - make sure all BPs have unique names
auth_bp = Blueprint('auth', __name__)

# this is a hint for a login function
@auth_bp.route('/login', methods=['GET', 'POST'])
# view function
def login():
    login_form = LoginForm()
    error = None
    if login_form.validate_on_submit():
        user_name = login_form.user_name.data
        password = login_form.password.data
        # Accept either email or first name in the username field.
        user = db.session.scalar(
            db.select(User).where(
                or_(User.email == user_name, User.first_name == user_name)
            )
        )
        if user is None:
            error = 'Incorrect user name'
        elif not check_password_hash(user.password, password): # takes the hash and cleartext password
            error = 'Incorrect password'
        if error is None:
            login_user(user)
            nextp = request.args.get('next') # this gives the url from where the login page was accessed
            if nextp is None or not nextp.startswith('/'):
                return redirect(url_for('main.index'))
            return redirect(nextp)
        else:
            flash(error)
    return render_template('user.html', form=login_form, heading='Login')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()

    if register_form.validate_on_submit():
        email = register_form.email.data.strip().lower()
        existing_user = db.session.scalar(db.select(User).where(User.email == email))

        if existing_user is not None:
            flash('Email is already registered. Please use a different email.')
            return render_template('register.html', form=register_form, heading='Register')

        hashed_password = generate_password_hash(register_form.password.data).decode('utf-8')
        user = User(
            first_name=register_form.first_name.data.strip(),
            last_name=register_form.last_name.data.strip(),
            email=email,
            password=hashed_password,
            Phone=register_form.contact_number.data.strip(),
            address=register_form.street_address.data.strip(),
        )

        db.session.add(user)
        db.session.commit()
        flash('Registration successful. You can now sign in.')
        return redirect(url_for('main.index'))

    return render_template('register.html', form=register_form, heading='Register')