from flask import Blueprint, render_template, redirect, \
    url_for, request, flash
from flask_login import login_user, logout_user, login_required
from flask_jwt_extended import create_access_token

from werkzeug.wrappers.response import Response
from werkzeug.security import generate_password_hash, check_password_hash

from loguru import logger


from .validators import User
from .models import User_ 
from . import db
from .db_operations import create_user, get_user

from entry_app import redis_db


auth = Blueprint('auth', __name__)

@auth.route('/login')
def login() -> str:
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post() -> Response:
    validated_user = User.model_validate(request.form.to_dict())
    user_from_db = get_user(validated_user.email)
    if not user_from_db or not check_password_hash(user_from_db.password, validated_user.password):
        flash('Проверьте правильно ли вы ввели пароль или логин')
        return redirect(url_for('auth.login'))
    login_user(user_from_db, remember=True)
    return redirect(url_for('main.profile'))


@auth.route('/register')
def register() -> str:
    return render_template('register.html')


@auth.route('/register', methods=['POST'])
def register_post() -> Response:
    validated_user = User.model_validate(request.form.to_dict())
    user_from_db = get_user(validated_user.email)
    if user_from_db:
        flash("Вы уже зарегистрировались")
        return redirect(url_for('auth.login'))
    new_user = create_user(validated_user)
    access_token = create_access_token(
        identity=new_user.email, 
        expires_delta=False
    )
    try:
        redis_db.set(new_user.email, access_token)
    except Exception as e:
        logger.exception(e)
    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout() -> Response:
    logout_user()
    return redirect(url_for('auth.login'))
