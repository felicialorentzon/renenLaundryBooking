from . import db
from .models import booking_table
from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

#redirect to the booking page if the user is signed in
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("/index.html", user=current_user)

#Updates the booking table for the client
@views.route('/refresh', methods=['GET', 'POST'])
@login_required
def sendBookingData():
    try:
        table_info = db.session.query(booking_table.date_and_time, booking_table.apartment_nb).all() 
        table_info_dict = [{'date_and_time': row.date_and_time, 'apartment_nb': row.apartment_nb} for row in table_info]
        return jsonify(table_info_dict)
    except:
        print("not ok")
        return [{"not ok": 0}]