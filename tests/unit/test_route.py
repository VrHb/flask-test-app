from flask import g, session
from flask_jwt_extended import create_access_token


def test_main_page(test_client):
    response = test_client.get('/')
    assert response.status_code == 302


def test_register(test_client):
    assert test_client.get('/register').status_code == 200
    response = test_client.post('/register',
        data={
            'name': 'User',
            'email': 'test@mail.com',
            'password': 'test'
        }
    )
    assert response.status_code == 302
    assert response.headers['Location'] == '/login'


def test_login(test_client, auth):
    assert test_client.get('/login').status_code == 200
    response = auth.login('test@mail.com', 'test')
    assert response.headers['Location'] == '/profile'
    assert session.get('_user_id') == '4'
    assert g.get('_login_user').email == 'test@mail.com'


def test_get_entries(test_client):
    assert test_client.get('/api/entries').status_code == 401
    assert test_client.post('/api/entries').status_code == 405
    assert test_client.put('/api/entries').status_code == 405
    assert test_client.delete('/api/entries').status_code == 405
    user_token = create_access_token('test@mail.com')
    headers = {
        'Authorization': f'Bearer {user_token}'
    }
    response = test_client.get('/api/entries', headers=headers)
    assert response.headers['Content-Type'] == 'application/json'
    assert response.status_code == 200


def test_post_entry(test_client):
    assert test_client.get('/api/entry').status_code == 405
    assert test_client.post('/api/entry').status_code == 401
    assert test_client.put('/api/entry').status_code == 405
    assert test_client.delete('/api/entry').status_code == 405
    user_token = create_access_token('test@mail.com')
    headers = {
        'Authorization': f'Bearer {user_token}'
    }
    payload = {
        'text': 'Some note!'
    }
    response = test_client.post('/api/entry', json=payload, headers=headers)
    assert response.headers['Content-Type'] == 'application/json'
    assert response.status_code == 200


def test_delete_entry(test_client):
    user_token = create_access_token('test@mail.com')
    headers = {
        'Authorization': f'Bearer {user_token}'
    }
    response = test_client.delete('/api/entry/999', headers=headers)
    assert response.status_code == 404
