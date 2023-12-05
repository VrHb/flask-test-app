from datetime import datetime
from werkzeug.security import generate_password_hash

from .validators import User, EntrySerializer
from .models import User_, Entry
from . import db

from loguru import logger


def get_user(email: str) -> User_ | None:
    user_from_db = User_.query.filter_by(email=email).first()
    return user_from_db


def create_user(user: User) -> User_:
    hashed_password = generate_password_hash(user.password)
    new_user = User_(
    name=user.name,
    email=user.email,
    password=hashed_password
    )
    db.session.add(new_user)
    db.session.commit()
    return new_user
    

def create_entry(user_email: str, entry_text: str) -> dict: 
    user = User_.query.filter_by(email=user_email).first_or_404()
    entry = Entry(
        user_id=user.id,
        text=entry_text
    )
    db.session.add(entry)
    db.session.commit()
    return EntrySerializer.model_validate(entry).model_dump()


def get_user_entries(user_email: str) -> list[dict]:
    user_entries_from_db = (
        User_.query
        .filter_by(email=user_email)
        .first_or_404()
        .entries
    )
    entries = [
        EntrySerializer.model_validate(entry).model_dump() for entry in user_entries_from_db
    ]
    return entries


def delete_entry_from_db(user_email: str, entry_id: int) -> dict:
    db_entry = (
        Entry.query
        .join(User_, Entry.user_id == User_.id)
        .filter(User_.email == user_email, Entry.id == entry_id)
        .first_or_404()
    )
    db.session.delete(db_entry)
    db.session.commit()
    return {
        'Deleted': EntrySerializer.model_validate(db_entry).model_dump()
    }


def update_entry_in_db(user_email: str, entry_id: int, new_text: str) -> dict:
    db_entry = (
        Entry.query
        .join(User_, Entry.user_id == User_.id)
        .filter(User_.email == user_email, Entry.id == entry_id)
        .first_or_404()
    )
    db_entry.text = new_text
    db.session.add(db_entry)
    db.session.commit()
    return {
        'Updated': EntrySerializer.model_validate(db_entry).model_dump()
    }
