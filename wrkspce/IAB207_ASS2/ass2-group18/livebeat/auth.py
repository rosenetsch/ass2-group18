from flask import Blueprint, flash, render_template, request, url_for, redirect
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, logout_user
from .models import User
from .forms import LoginForm, RegisterForm
from . import db

# Create a blueprint - make sure all BPs have unique names
auth_bp = Blueprint('auth', __name__)


# view function
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        email = login_form.email.data.strip().lower()
        password = login_form.password.data

        user = db.session.scalar(
            db.select(User).where(User.email == email)
        )

        if user is None:
            flash('Incorrect email address')
            return render_template('user.html', form=login_form, heading='Login')

        if not check_password_hash(user.password, password):
            flash('Incorrect password')
            return render_template('user.html', form=login_form, heading='Login')

        login_user(user)

        nextp = request.args.get('next')
        if nextp is None or not nextp.startswith('/'):
            return redirect(url_for('main.index'))

        return redirect(nextp)

    return render_template('user.html', form=login_form, heading='Login')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


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
            phone=register_form.contact_number.data.strip(),
            address=register_form.street_address.data.strip(),
        )

        db.session.add(user)
        db.session.commit()
        flash('Registration successful. You can now sign in.')
        return redirect(url_for('main.index'))

    return render_template('register.html', form=register_form, heading='Register')