import json

from contextvars import Token
from datetime import datetime

from flask import Blueprint, render_template, redirect, \
    url_for, jsonify, request
from flask_login import login_required, current_user
from flask_jwt_extended import get_jwt_identity, jwt_required

from werkzeug.wrappers.response import Response

from loguru import logger

from . import db
from .models import User_, Entry

from entry_app import redis_db



main = Blueprint('main', __name__)

@main.route('/')
def index():
    return redirect(url_for('auth.register')) 


@main.route('/profile')
@login_required
def profile() -> str:
    entries_from_db = Entry.query.filter_by(user_id=current_user.id).all()   
    entries = [entry.text for entry in entries_from_db]
    user_token = redis_db.get(current_user.email)
    return render_template(
        'profile.html',
        name=current_user.name,
        entries=entries,
        token=user_token 
    )


@main.route('/api/entry', methods=["POST"])
@jwt_required()
def add_entry() -> tuple[Response, int]:
    user_email = get_jwt_identity()
    user = User_.query.filter_by(email=user_email).first_or_404()
    entry_date = datetime.now()
    entry_text = request.json.get('text')
    new_entry = Entry(
        user_id=user.id,
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
    user_email = get_jwt_identity()
    db_user_entries = User_.query.filter_by(email=user_email).first_or_404().entries
    entries = [{'id': entry.id, 'text': entry.text} for entry in db_user_entries]
    return jsonify(entries), 200


@main.route('/api/entry/<int:entry_id>', methods=['DELETE'])
@jwt_required()
def delete_entry(entry_id: int) -> tuple[Response, int]:
    user_email = get_jwt_identity()
    # TODO optimize queries
    db_user = User_.query.filter_by(email=user_email).first_or_404()
    db_entry = Entry.query.filter_by(user_id=db_user.id, id=entry_id).first_or_404()
    logger.info(db_entry)
    db.session.delete(db_entry)
    db.session.commit()
    return jsonify({'message': 'entry delete!'}), 200


@main.route('/api/entry/<int:entry_id>', methods=['PUT'])
@jwt_required()
def update_entry(entry_id: int) -> tuple[Response, int]:
    user_email = get_jwt_identity()
    # TODO optimize queries
    db_user = User_.query.filter_by(email=user_email).first_or_404()
    db_entry = Entry.query.filter_by(user_id=db_user.id, id=entry_id).first_or_404()
    new_text = request.json.get('text') 
    db_entry.text = new_text
    db.session.add(db_entry)
    db.session.commit()
    return jsonify('ok'), 200
