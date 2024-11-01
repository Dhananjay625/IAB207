import random
from flask import Blueprint, flash, render_template, request, url_for, redirect
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from .models import User
from .forms import LoginForm, RegisterForm
from . import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    error = None
    print(login_form.validate_on_submit())
    if login_form.validate_on_submit():
        user_name = login_form.user_name.data
        password = login_form.password.data
        user = db.session.scalar(db.select(User).where(User.username == user_name)) 
        print(user_name)
        print(password)
        
        if user is None:
            error = 'Account does not exist.'

        elif not check_password_hash(user.password, password):  
            error = 'Incorrect password.'
        
        if error is None:
            login_user(user)
            nextp = request.args.get('next')
            if not nextp or not nextp.startswith('/'):
                return redirect(url_for('main.homepage'))
            return redirect(nextp)
        else:
            flash(error)
    return render_template('login.html', form=login_form, heading='Login')
    
@auth_bp.route('/logout')
@login_required  
def logout():
    logout_user()  
    return redirect(url_for('main.homepage'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()

    if request.method == 'POST' and register_form.validate_on_submit():
        username = register_form.user_name.data
        email = register_form.email.data
        password = register_form.password.data
        contact_number = register_form.contact_number.data
        address = register_form.address.data

        if password != register_form.confirm_password.data:
            flash('Passwords do not match.')
            return render_template('register.html', form=register_form)

        existing_user = db.session.scalar(db.select(User).where((User.username == username) | (User.email == email)))
        if existing_user:
            flash('Username or email already exists.')
            return render_template('register.html', form=register_form)

        while True:
            user_id = random.randint(1000, 9999)
            existing_user = db.session.scalar(db.select(User).where(User.id == user_id))
            if existing_user is None:
                break

        new_user = User(
            id=user_id, username=username, email=email,
            password=generate_password_hash(password),
            contact_number=contact_number, address=address
        )
        
        db.session.add(new_user)

        try:
            db.session.commit()
            flash('Registration successful! Please log in.')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred: {e}")
            return render_template('register.html', form=register_form)

    return render_template('register.html', form=register_form)
