from . import db
from flask_login import UserMixin

#Table for bookable time slots
class booking_table(db.Model):
    date_and_time = db.Column(db.String(20), primary_key=True)
    apartment_nb = db.Column(db.Integer, index = True, unique = False)

#Table for user info
class user(UserMixin, db.Model):
    apartment_nb = db.Column(db.Integer, primary_key=True)
    pin = db.Column(db.String(256), index = False, unique=False)

    def get_id(self):
        return self.apartment_nb