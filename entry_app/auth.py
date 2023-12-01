from flask import Blueprint, render_template, redirect, url_for, request

from werkzeug.wrappers.response import Response
from werkzeug.security import generate_password_hash

from loguru import logger

from .models import User_ 
from . import db


auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return 'Login'


@auth.route('/register')
def register():
    return render_template('register.html')


@auth.route('/register', methods=['POST'])
def register_post() -> Response:
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password', 'empty')
    hashed_password = generate_password_hash(password)
    user = User_.query.filter_by(email=email).first()
    if user:
        return redirect(url_for('auth.register'))
    new_user = User_(
    name=name,
    email=email,
    password=hashed_password
    )
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('auth.login'))


@auth.route('/logout')
def logout():
    return 'Logout'
