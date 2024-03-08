from . import db
from .models import BookingTable
from .models import User
from flask import Blueprint, render_template, request, flash, jsonify
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
    if request.method == 'POST': 
        note = request.form.get('note')

        if note and len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = BookingTable(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("/index.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data)
    noteId = note['noteId']
    note = BookingTable.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
