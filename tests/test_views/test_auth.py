"""
    Test the Authentication view
    Auth: Peter S. Zyambo
"""
import pytest
from flask import g, session
from lipila.db import get_db

# test register route
def test_register(client, app):
    assert client.get('/auth/register/schools').status_code == 200
    response = client.post(
        '/auth/register/schools', data={
            'job':'ab', 'school':'b', 'email':'b',
            'mobile':'b', 'reg_number':'b', 'firstname':'b',
            'lastname':'b', 'password':'b'}
    )
    assert response.headers["Location"] == "/auth/login/schools"

    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM school WHERE email = 'b'",
        ).fetchone() is not None


@pytest.mark.parametrize((
    'job', 'school', 'email', 'mobile', 'reg_number',
    'firstname', 'lastname', 'password', 'message'), (
    ('', '','','','','','','', b'School is required.'),
    ('admin', 'academy','','','','','','', b'Mobile is required.'),
    ('a', 'a','a','a','a','a','a','a', b'already registered.'),
))
def test_register_validate_input(
    client, job, school, email, mobile, reg_number,
    firstname, lastname, password, message):
    response = client.post(
        '/auth/register/schools',
        data={
            'job':job, 'school':school, 'email':email,
            'mobile':mobile, 'reg_number':reg_number, 'firstname':firstname,
            'lastname':lastname, 'password':password}
    )
    assert message in response.data
    assert response.status_code == 200

# test login route
def test_login(client, auth):
    assert client.get('/auth/login/schools').status_code == 200
    response = auth.login()
    assert response.headers["Location"] == "/lipila/admin/dashboard"

    with client:
        client.get('/auth/login/schools')
        assert session['user_id'] == 1
        assert g.user['email'] == 'pz@email.com'


@pytest.mark.parametrize(('email', 'password', 'message'), (
    ('a', 'test', b'Incorrect credentials. Please check your details'),
    ('test', 'a', b'Incorrect credentials. Please check your details'),
))
def test_login_validate_input(auth, email, password, message):
    response = auth.login(email, password)
    assert message in response.data

def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session