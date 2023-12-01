from flask import Blueprint, render_template, redirect, \
    url_for, request, flash
from flask_login import login_user, logout_user, login_required

from werkzeug.wrappers.response import Response
from werkzeug.security import generate_password_hash, check_password_hash

from loguru import logger

from .models import User_ 
from . import db


auth = Blueprint('auth', __name__)

@auth.route('/login')
def login() -> str:
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post() -> Response:
    email = request.form.get('email')
    password = request.form.get('password', 'empty')
    user = User_.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash('Проверьте правильно ли вы ввели пароль или логин')
        return redirect(url_for('auth.login'))
    login_user(user, remember=True)
    return redirect(url_for('main.profile'))


@auth.route('/register')
def register() -> str:
    return render_template('register.html')


@auth.route('/register', methods=['POST'])
def register_post() -> Response:
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password', 'empty')
    hashed_password = generate_password_hash(password)
    user = User_.query.filter_by(email=email).first()
    if user:
        flash("Вы уже зарегистрировались")
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
@login_required
def logout() -> Response:
    logout_user()
    return redirect(url_for('auth.login'))
