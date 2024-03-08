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
            login_user(user, remember=True)
            flash('', category='success') #remove potential past error messages
            return redirect(url_for('views.home'))
        else:
            flash('Incorrect pin, try again.', category='error')
    else:
        flash('apartment_nb does not exist.', category='error')
    return redirect(url_for('auth.login'))

@auth.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

#@auth.route('/book', methods=['POST'])
#def booking():
    #date = request.form.get('ConfirmTime')
    ##Får None när jag försöker printa ut date i terminalen
    ##Kan det vara att det är i en <p> och ej <input>??
    ##Får kolla vad <from> egentligen tar med sig till servern
    #print("Date: " + str(date))
    #apartment_nb = request.form.get('apartment_nb') #fixa date först. 
    #return redirect(url_for('views.home'))