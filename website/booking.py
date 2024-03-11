from flask import Blueprint, request, redirect, url_for

book = Blueprint('booking', __name__)

@book.route('/book', methods=['GET', 'POST'])
def booking():
    date = request.form.get('inputConfirmTime')
    apartment_nb = request.form.get('apNr')
    print("Apartment number: " + str(apartment_nb)) 
    print("Date: " + str(date))
    return redirect(url_for('views.home'))