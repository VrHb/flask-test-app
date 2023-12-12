import os 
import pytest 

from entry_app import create_app
from entry_app.models import User_


class AuthAction(object):
    def __init__(self, client):
        self._client = client


    def login(self, email, password):
        return self._client.post(
            '/login',
            data={'email': email, 'password': password}
        )


    def logout(self):
        self._client.get('/logout')


@pytest.fixture
def auth(test_client):
    return AuthAction(test_client)


@pytest.fixture(scope='module')
def new_user():
    user = User_(
        name='Alena',
        email='alena@mail.com',
        password='new_pass',
    )
    return user


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()
    flask_app.config.update({
        'TESTING': True,
    })
    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client  
