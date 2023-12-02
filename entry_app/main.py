from datetime import datetime

from flask import Blueprint, render_template, redirect, \
    url_for, jsonify, request
from flask_login import login_required, current_user
from flask_jwt_extended import get_jwt_identity, jwt_required

from werkzeug.wrappers.response import Response

from loguru import logger

from . import db
from .models import User_, Entry


main = Blueprint('main', __name__)

@main.route('/')
def index():
    return redirect(url_for('auth.register')) 


@main.route('/profile')
@login_required
def profile() -> str:
    entries_from_db = Entry.query.filter_by(user_id=current_user.id).all()   
    entries = [entry.text for entry in entries_from_db]
    return render_template('profile.html', name=current_user.name, entries=entries)


@main.route('/api/entry', methods=["POST"])
@jwt_required()
def add_entry() -> tuple[Response, int]:
    user_id = get_jwt_identity()
    user = User_.query.get_or_404(user_id)
    entry_date = datetime.now()
    entry_text = request.json.get('text')
    new_entry = Entry(
        user_id=user_id,
        date=entry_date,
        text=entry_text
            )
    db.session.add(new_entry)
    db.session.commit()
    # TODO serialize entry object
    entry = {
        'text': new_entry.text,
        'creation_date': new_entry.date,
        'user-id': new_entry.user_id
    }
    return jsonify(entry), 200


@main.route('/api/entries', methods=['GET'])
@jwt_required()
def get_entries() -> tuple[Response, int]:
    user_id = get_jwt_identity()
    entries_from_db = Entry.query.filter_by(user_id=user_id).all()   
    entries = [{'id': entry.id, 'text': entry.text} for entry in entries_from_db]
    return jsonify(entries), 200


@main.route('/api/entry/<int:entry_id>', methods=['DELETE'])
@jwt_required()
def delete_entry(entry_id: int) -> tuple[Response, int]:
    user_id = get_jwt_identity()
    entry = Entry.query.filter_by(user_id=user_id, id=entry_id).first_or_404()
    db.session.delete(entry)
    db.session.commit()
    return jsonify({'message': 'entry delete!'}), 200


@main.route('/api/entry/<int:entry_id>', methods=['PUT'])
@jwt_required()
def update_entry(entry_id: int) -> tuple[Response, int]:
    user_id = get_jwt_identity()
    entry = Entry.query.filter_by(user_id=user_id, id=entry_id).first_or_404()
    new_text = request.json.get('text')
    entry.text = new_text
    db.session.add(entry)
    db.session.commit()
    return jsonify('ok'), 200

    

    

