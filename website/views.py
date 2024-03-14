from . import db
from .models import booking_table
from .models import user
from flask import Blueprint, render_template, request, flash, json, jsonify
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@views.route('/test', methods=['GET'])
def test():
    users = db.session.execute(db.select(user).order_by(user.apartment_nb)).scalars() #så man ska fråga (SQL)
    for cuser in users:
        print(cuser.apartment_nb)
    return render_template("index.html")

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    #add refresh here so that server sends everyting in booking_table_data to javascript.
    #javascript then needs to update all the dates and availability status according to db,
    #which we have yet to create in index.html

    return render_template("/index.html", user=current_user)

@views.route('/refresh', methods=['GET', 'POST'])
@login_required
def sendBookingData():
    try:
        table_info = db.session.query(booking_table.date_and_time, booking_table.apartment_nb).all() #list
        #print(table_info)
        table_info_dict = [{'date_and_time': row.date_and_time, 'apartment_nb': row.apartment_nb} for row in table_info]
        return jsonify(table_info_dict)
    except:
        print("not ok")
        return [{"not ok": 0}]