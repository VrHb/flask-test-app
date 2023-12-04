from datetime import datetime

from entry_app.models import User_, Entry


def test_new_user():
    '''
    GIVEN a user model
    WHEN a new user created
    THEN check model fields are defined correctly
    '''
    user = User_(
        name='Alena',
        email='alena@mail.com',
        password='',
    )
    assert user.name == 'Alena'
    assert user.email == 'alena@mail.com'
    assert user.password == ''


def test_new_entry():
    '''
    GIVEN a entry model
    WHEN a new entry created
    THEN check model fields are defined corrrectly
    '''
    user = User_(
        name='Alena',
        email='alena@mail.com',
        password='',
    )
    creation_date = datetime.now()
    entry = Entry(
        user_id=user.id,
        date=creation_date,
        text='Some text',
    )
    assert entry.user_id == user.id 
    assert entry.date == creation_date
    assert entry.text == 'Some text'
