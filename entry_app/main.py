from flask import Blueprint, render_template, redirect, url_for
from . import db


main = Blueprint('main', __name__)

@main.route('/')
def index():
    return redirect(url_for('auth.register')) 


@main.route('/profile')
def profile():
    return 'Profile'
