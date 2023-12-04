from entry_app import create_app
from flask_jwt_extended import get_jwt_identity, create_access_token


def test_get_token_page_not_logged_in():
    '''
    GIVEN test flask-app configured for testing 
    WHEN the main page requested if user not loggged in (GET)
    THEN check redirect to login page
    '''
    flask_app = create_app()
    with flask_app.test_client() as test_client:
        response = test_client.get('/profile')
        assert response.status_code == 302


def test_create_entry_api_unauth(test_client):
    '''
    GIVEN test flask-app configured for testing
    WHEN the create entry without token 
    THEN check the status code
    '''
    access_token = create_access_token(
        identity='user_id',
        expires_delta=False
    )
    response = test_client.post(
            '/api/entry',
            # headers={'Authentification': f'Bearer {access_token}'},
            data={
                'text': 'Some text!'
            }
        )
    assert response.status_code == 401 



