import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from dotenv import load_dotenv


db = SQLAlchemy()


def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') 
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')    
    # TODO add postgres url

    db.init_app(app)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
