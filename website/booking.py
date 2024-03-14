from flask import Blueprint, request, redirect, url_for
from . import db
from sqlalchemy import text
from .models import booking_table

book = Blueprint('booking', __name__)

@book.route('/book', methods=['GET', 'POST'])
def booking():
    #uppdatera databasen
    date = request.form.get('inputConfirmTime')
    date_table_format = text(date[8] + date[9] + date[10] + date[11] + date[12] + date[13]+ '|' + date[0] + date[1] + date[2] + date[3] + date[4])
    apartment_nb = request.form.get('apNr')
    print("Apartment number: " + str(apartment_nb))
    print("Date: " + str(date))
    #print(db.Query(db.column(date_table_format) + "from booking_table"))
    #print(db.Query.get_or_404(date_table_format))
    #print(db.Query.all(book))#db.session.execute(db.text(f'select {date_table_format} from booking_table')))
    db_request = db.session.execute(db.select(date_table_format))
    print("db_request: " + str(db_request))
    for row in db_request:
        #substring ta bort 1 fram 2 bak.
        if(row == -3):
            print("ok")
        print("row: " + str(row))
        #print("row.index(): " + str(row.index(0)))
        #print("row.count(): " + str(row.count()))

    
    print(db_request.mappings().all()) #.order_by(date_table_format.apartment_nb)).scalars())
    print(db_request.mappings())

    users = db.session.execute(db.select(booking_table).order_by(booking_table.apartment_nb)).scalars() #så man ska fråga (SQL)
    #for cuser in users:
        #print(cuser.apartment_nb)
    
    #print(db_request.values())

    return redirect(url_for('views.home'))