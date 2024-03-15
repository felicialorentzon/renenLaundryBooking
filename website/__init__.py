from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from os import path
from werkzeug.security import generate_password_hash
from passlib.hash import sha256_crypt

db = SQLAlchemy()
DB_NAME = "laundry_booking.db"

def create_app():
    app = Flask(__name__, static_url_path='', static_folder='static')
    app.config['SECRET_KEY'] = 'very secret key'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .booking import book

    app.register_blueprint(book, url_prefix='/')
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import user
    from .models import booking_table
    
    # db requires flask app context to create tables
    with app.app_context():
        # create tables
        db.create_all()

        # create data to later insert
        login_table_data = [
            user(pin = generate_password_hash("2748", method='pbkdf2:sha256'), apartment_nb = 1101),
            user(pin = generate_password_hash("3953", method='pbkdf2:sha256'), apartment_nb = 1102),
            user(pin = generate_password_hash("8462", method='pbkdf2:sha256'), apartment_nb = 1201),
            user(pin = generate_password_hash("5792", method='pbkdf2:sha256'), apartment_nb = 1202),
            user(pin = generate_password_hash("8563", method='pbkdf2:sha256'), apartment_nb = 1301),
            user(pin = generate_password_hash("2622", method='pbkdf2:sha256'), apartment_nb = 1302),
        ]
        #day-month|start time-end time
        booking_table_data = [
            booking_table(date_and_time = '18-03|08-11', apartment_nb = None),
            booking_table(date_and_time = '18-03|11-14', apartment_nb = None),
            booking_table(date_and_time = '18-03|14-17', apartment_nb = None),
            booking_table(date_and_time = '18-03|17-20', apartment_nb = None),
            booking_table(date_and_time = '19-03|08-11', apartment_nb = None),
            booking_table(date_and_time = '19-03|11-14', apartment_nb = None),
            booking_table(date_and_time = '19-03|14-17', apartment_nb = None),
            booking_table(date_and_time = '19-03|17-20', apartment_nb = None),
            booking_table(date_and_time = '20-03|08-11', apartment_nb = None),
            booking_table(date_and_time = '20-03|11-14', apartment_nb = None),
            booking_table(date_and_time = '20-03|14-17', apartment_nb = None),
            booking_table(date_and_time = '20-03|17-20', apartment_nb = None),
            booking_table(date_and_time = '21-03|08-11', apartment_nb = None),
            booking_table(date_and_time = '21-03|11-14', apartment_nb = None),
            booking_table(date_and_time = '21-03|14-17', apartment_nb = None),
            booking_table(date_and_time = '21-03|17-20', apartment_nb = None),
            booking_table(date_and_time = '22-03|08-11', apartment_nb = None),
            booking_table(date_and_time = '22-03|11-14', apartment_nb = None),
            booking_table(date_and_time = '22-03|14-17', apartment_nb = None),
            booking_table(date_and_time = '22-03|17-20', apartment_nb = None),
            booking_table(date_and_time = '23-03|08-11', apartment_nb = None),
            booking_table(date_and_time = '23-03|11-14', apartment_nb = None),
            booking_table(date_and_time = '23-03|14-17', apartment_nb = None),
            booking_table(date_and_time = '23-03|17-20', apartment_nb = None),
            booking_table(date_and_time = '24-03|08-11', apartment_nb = None),
            booking_table(date_and_time = '24-03|11-14', apartment_nb = None),
            booking_table(date_and_time = '24-03|14-17', apartment_nb = None),
            booking_table(date_and_time = '24-03|17-20', apartment_nb = None)
        ]


        # insert data
        for item in login_table_data:
            db.session.add(item)
        try:
            # see if it successfully can insert
            db.session.commit()
        except Exception:
            # otherwise rollback changes
            db.session.rollback()

        for item in booking_table_data:
            db.session.add(item)
        try:
            # see if it successfully can insert
            db.session.commit()
        except Exception:
            # otherwise rollback changes
            db.session.rollback()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return db.session.execute(db.select(user).where(user.apartment_nb == id)).scalar()

    return app