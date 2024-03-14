from flask import Blueprint, request, redirect, url_for
from . import db

book = Blueprint('booking', __name__)

@book.route('/book', methods=['GET', 'POST'])
def booking():
    #uppdatera databasen
    date = request.form.get('inputConfirmTime')
    date2 = (str(date))
    apartment_nb = request.form.get('apNr')
    print("Apartment number: " + str(apartment_nb))
    print("Date: " + str(date))
    #print(db.session.execute(db.select(date2).order_by(date2.apartment_nb)).scalars())

    return redirect(url_for('views.home'))