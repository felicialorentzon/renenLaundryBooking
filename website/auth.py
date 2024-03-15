from .models import user
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
from . import db

auth = Blueprint('auth', __name__)

#Route for the login page and the redirect if the login succeeds 
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
    current_user = db.session.execute(db.select(user).where(user.apartment_nb == apartment_nb)).scalar()

    if current_user:
        if pin and check_password_hash(current_user.pin, pin):
            login_user(current_user, remember=True)
            flash('', category='success') #remove potential past error messages
            return redirect(url_for('views.home'))
        else:
            flash('Felaktig PIN-kod, försök igen.', category='error')
    else:
        flash('Lägenhetsnumret finns inte, vänligen ange korrekt nummer.', category='error')
    return redirect(url_for('auth.login'))

#Handle the logout
@auth.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
