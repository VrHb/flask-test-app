from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

from . import db


main = Blueprint('main', __name__)

@main.route('/')
def index():
    return redirect(url_for('auth.register')) 


@main.route('/profile')
@login_required
def profile() -> str:
    return render_template('profile.html', name=current_user.name)
