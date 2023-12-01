import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from dotenv import load_dotenv


db = SQLAlchemy()


def create_app() -> Flask:
    load_dotenv()
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') 
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')    

    db.init_app(app)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User_

    @login_manager.user_loader
    def load_user(user_id):
        return User_.query.get(int(user_id))

    from . import models
    with app.app_context():
        db.create_all()


    return app
