from . import db
from .models import BookingTable
from .models import User
from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
import json

views = Blueprint('views', __name__)

@views.route('/test', methods=['GET'])
def test():
    users = db.session.execute(db.select(User).order_by(User.apartment_nb)).scalars() #så man ska fråga (SQL)
    for user in users:
        print(user.apartment_nb)
    return render_template("index.html")

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    #add refresh here so that server sends everyting in booking_table_data to javascript.
    #javascript then needs to update all the dates and availability status according to db,
    #which we have yet to create in index.html
    return render_template("/index.html", user=current_user)

