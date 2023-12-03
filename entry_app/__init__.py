import os

import redis

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from celery import Celery, Task

from dotenv import load_dotenv


db = SQLAlchemy()

redis_db = redis.Redis(
    host=os.getenv('REDIS_HOST'),
    port=os.getenv('REDIS_PORT'),
    decode_responses=True
)


def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app


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

    # TODO in doc use JWT_SECRET-KEY is same as SECRET_KEY?
    # TODO use JWT token expires env
    jwt_manager = JWTManager(app)

    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User_

    @login_manager.user_loader
    def load_user(user_id):
        return User_.query.get(int(user_id))

    app.config.from_mapping(
        CELERY=dict(
            broker_url=os.getenv('CELERY_BROKER'), 
            result_backend=os.getenv('CELERY_RESULT_BACKEND'), 
            task_ignore_result=True,
        ),
    )
    celery_init_app(app)

    from . import models
    with app.app_context():
        db.create_all()


    return app
