from flask import Blueprint, render_template, redirect, \
    url_for, jsonify, request
from flask_login import login_required, current_user
from flask_jwt_extended import get_jwt_identity, jwt_required

from werkzeug.wrappers.response import Response

from .db_operations import create_entry, get_user_entries, \
    delete_entry_from_db, update_entry_in_db

from entry_app import redis_db



main = Blueprint('main', __name__)

@main.route('/')
def index():
    return redirect(url_for('auth.register')) 


@main.route('/profile')
@login_required
def profile() -> str:
    serialized_entries = get_user_entries(current_user.email)   
    entries = [entry.get('text') for entry in serialized_entries]
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
    entry_text = request.json.get("text")
    user_email = get_jwt_identity()
    new_entry = create_entry(user_email, entry_text)
    return jsonify(new_entry), 200


@main.route('/api/entries', methods=['GET'])
@jwt_required()
def get_entries() -> tuple[Response, int]:
    user_email = get_jwt_identity()
    entries = get_user_entries(user_email)
    return jsonify(entries), 200


@main.route('/api/entry/<int:entry_id>', methods=['DELETE'])
@jwt_required()
def delete_entry(entry_id: int) -> tuple[Response, int]:
    user_email = get_jwt_identity()
    deleted_entry_info = delete_entry_from_db(user_email, entry_id)
    return jsonify(deleted_entry_info), 200


@main.route('/api/entry/<int:entry_id>', methods=['PUT'])
@jwt_required()
def update_entry(entry_id: int) -> tuple[Response, int]:
    user_email = get_jwt_identity()
    new_text = request.json.get('text')
    updated_entry_info = update_entry_in_db(user_email, entry_id, new_text)
    return jsonify(updated_entry_info), 200
