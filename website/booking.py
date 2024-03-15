from flask import Blueprint, request, redirect, url_for
from . import db
from .models import booking_table

book = Blueprint('booking', __name__)

@book.route('/book', methods=['GET', 'POST'])
def booking():
    #uppdatera databasen
    date = request.form.get('inputConfirmTime')
    print(date)
    month_txt = date[13] + date[14] + date[15]

    match month_txt:
        case "Jan": month_nb = "01"
        case "Feb": month_nb = "02"
        case "Mar": month_nb = "03"
        case "Apr": month_nb = "04"
        case "Maj": month_nb = "05"
        case "Jun": month_nb = "06"
        case "Jul": month_nb = "07"
        case "Aug": month_nb = "08"
        case "Sep": month_nb = "09"
        case "Okt": month_nb = "10"
        case "Nov": month_nb = "11"
        case "Dec": month_nb = "12"
    
    date_table_format = (date[10] + date[11] + "-" + month_nb + '|' + date[0] + date[1] + date[2] + date[3] + date[4]).strip()
    print(date_table_format)
    try:
        apartment_nb = int(request.form.get('apNr').strip())
    except ValueError:
        print("Error: The apartment number is not a number.")
        return redirect(url_for('views.home'))
        
    user_from_database = db.session.query(booking_table).filter(booking_table.date_and_time == date_table_format).first()

    if user_from_database is None:
        print(f'Error: The time slot f{user_from_database} does not exist.')
        return redirect(url_for('views.home'))

    if user_from_database.apartment_nb == apartment_nb:
        user_from_database.apartment_nb = None
        db.session.commit()
        print("Booking cancelled!")
        return redirect(url_for('views.home'))

    if user_from_database.apartment_nb is not None:
        print("Error: The time slot is already booked. Please choose another time.")
        return redirect(url_for('views.home'))
    print("Booking successful!")
    user_from_database.apartment_nb = apartment_nb
    db.session.commit()

    return redirect(url_for('views.home'))