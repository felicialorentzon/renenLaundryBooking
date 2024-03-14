from flask import Blueprint, request, redirect, url_for
from . import db
from .models import booking_table

book = Blueprint('booking', __name__)

# @book.route('/hahalol')
# def hahalol():
#    return json.dumps(db.session.query(booking_table).all())
#
# async function fetchHaha() {
#     const res = await fetch('/hahalol')
#     // error handling
#     if (!res.ok) {
#         throw new Error('Network response was not ok')
#     }
#     // parse the response
#     const data =  res.json()
#     console.log(data)
# }

@book.route('/book', methods=['GET', 'POST'])
def booking():
    #uppdatera databasen
    date = request.form.get('inputConfirmTime')
    date_table_format = (date[8] + date[9] + date[10] + date[11] + date[12] + date[13]+ '|' + date[0] + date[1] + date[2] + date[3] + date[4]).strip()

    try:
        apartment_nb = int(request.form.get('apNr').strip())
    except ValueError:
        # TODO: change to a response for the javascript
        print("Error: The apartment number is not a number.")
        return redirect(url_for('views.home'))
        
    res = db.session.query(booking_table).filter(booking_table.date_and_time == date_table_format).first()

    if res is None:
        # TODO: change to a response for the javascript
        print("Error: The time slot does not exist.")
        return redirect(url_for('views.home'))

    if res.apartment_nb == apartment_nb:
        res.apartment_nb = None
        db.session.commit()
        # TODO: change to a response for the javascript
        print("Booking cancelled!")
        return redirect(url_for('views.home'))

    if res.apartment_nb is not None:
        # TODO: change to a response for the javascript
        print("Error: The time slot is already booked. Please choose another time.")
        return redirect(url_for('views.home'))

    # TODO: change to a response for the javascript
    print("Booking successful!")
    res.apartment_nb = apartment_nb
    db.session.commit()

    return redirect(url_for('views.home'))