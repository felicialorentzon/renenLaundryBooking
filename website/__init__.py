from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from os import path
from werkzeug.security import generate_password_hash

db = SQLAlchemy()
DB_NAME = "laundry_booking.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'very secret key'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User
    from .models import Note
    
    # db requires flask app context to create tables
    with app.app_context():
        # create tables
        db.create_all()

        # create data to later insert
        login_table_data = [
            User(pin = generate_password_hash("2748"), apartment_nb = 1101),
            User(pin = generate_password_hash("3953"), apartment_nb = 1102),
            User(pin = generate_password_hash("8462"), apartment_nb = 1201),
            User(pin = generate_password_hash("5792"), apartment_nb = 1202),
            User(pin = generate_password_hash("8563"), apartment_nb = 1301),
            User(pin = generate_password_hash("2622"), apartment_nb = 1302),
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

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return db.session.execute(db.select(User).where(User.apartment_nb == id)).scalar()

    return app