from flask import Blueprint
from . import db


auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return 'Login'


@auth.route('/singup')
def singup():
    return 'Singnup'


@auth.route('/logout')
def logout():
    return 'Logout'