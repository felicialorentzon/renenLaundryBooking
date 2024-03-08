from .models import User
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    else:
        return render_template("login.html", user=current_user)

@auth.route('/login', methods=['POST'])
def handle_login():
    apartment_nb = request.form.get('apartment_nb')
    pin = request.form.get('pin')
    user = db.session.execute(db.select(User).where(User.apartment_nb == apartment_nb)).scalar()

    if user:
        if pin and check_password_hash(user.pin, pin):
            flash('Logged in successfully!', category='success')
            login_user(user, remember=True)
            return redirect(url_for('views.home'))
        else:
            flash('Incorrect pin, try again.', category='error')
    else:
        flash('apartment_nb does not exist.', category='error')
    return redirect(url_for('auth.login'))

@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))