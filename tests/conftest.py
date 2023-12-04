import pytest 

from entry_app import create_app
from entry_app.models import User_


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

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client  
