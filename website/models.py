from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class BookingTable(db.Model):
    date_and_time = db.Column(db.String(50), primary_key=True)
    apartment_nb = db.Column(db.Integer, index = True, unique = False)

class User(UserMixin, db.Model):
    apartment_nb = db.Column(db.Integer, primary_key=True)
    pin = db.Column(db.String(128), index = False, unique=False)

    def get_id(self):
        return self.apartment_nb