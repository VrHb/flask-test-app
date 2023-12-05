from sqlalchemy.sql import func
from flask_login import UserMixin

from . import db


class User_(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    email = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(200))

    def __str__(self) -> str:
        return (
            f'User {self.name} with e-mail: {self.email}\n'
        )

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user_.id'),
        nullable=False
    )
    user = db.relationship(
        'User_',
        backref=db.backref('entries', lazy=True)
    )
    date = db.Column(db.DateTime(), server_default=func.now())
    text = db.Column(db.String(255), nullable=False)

    def __str__(self) -> str:
       return (
           f'entry for user {self.user_id}\n'
           f'With text: {self.text}\n'
           f'date entry: {self.date}\n'
       )
