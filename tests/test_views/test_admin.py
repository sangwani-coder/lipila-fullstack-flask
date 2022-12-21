"""
    Test the admin view
    Auth: Peter S. Zyambo
"""
import pytest
from skoolpay.db import get_db
from flask import g, session


def test_dashbord(client, auth):
    response = auth.login()
    assert response.headers["Location"] == "/skoolpay/admin/dashboard"

    with client:
        res = client.get('/skoolpay/admin/dashboard')
        assert session['user_id'] == 1
        assert g.user['email'] == 'pz@email.com'
        assert b'pz@email.com' in res.data
        assert b'Log Out' in res.data
        assert b'<h1>DASHBOARD</h1>' in res.data


def test_create_student(client, auth, app):
    """ test the add_student route and methods"""
    response = auth.login()
    assert response.headers['Location'] == '/skoolpay/admin/dashboard'
    with client:
        assert client.get('/skoolpay/admin/add').status_code == 200

    response = client.post(
        '/skoolpay/admin/add', data={
            'firstname':'ab', 'lastname':'b', 'school':1,
            'program':'b', 'tuition':300,
            }
    )
    # assert response.headers['Location'] == '/skoolpay/admin/dashboard'
    assert b'student added successfully.' in response.data

    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM student WHERE firstname = 'ab'",
        ).fetchone() is not None


@pytest.mark.parametrize((
    'firstname', 'lastname', 'school', 'program', 'tuition', 'message'), (
    ('', '','','','', b'firstname is required'),
    ('p', '','','','', b'lastname is required'),
    ('p', 'z',1,'se','', b'tuition is required'),
))
def test_create_student_validate_input(
    client, auth, firstname, lastname, school, program, tuition, message):
    response = auth.login()
    assert response.headers['Location'] == '/skoolpay/admin/dashboard'
    with client:
        assert client.get('/skoolpay/admin/add').status_code == 200
    response = client.post(
        '/skoolpay/admin/add',
        data={
            'firstname':firstname, 'lastname':lastname, 'school':school,
            'program':program, 'tuition':tuition}
    )
    assert response.status_code == 200
    assert message in response.data

def test_show_students(client, auth, app):
    """ Test ths route to return registered students"""
    response = auth.login()
    assert response.headers['Location'] == '/skoolpay/admin/dashboard'
    with client:
        assert client.get('/skoolpay/admin/students').status_code == 200
        assert session['email'] == 'pz@email.com'

    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM student WHERE school =1"
        ).fetchall() is not None

def test_list_payments(client, auth):
    """ Test ths route to return registered students"""
    response = auth.login()
    assert response.headers['Location'] == '/skoolpay/admin/dashboard'
    with client:
        response = client.get('/skoolpay/admin/payments')
        assert response.status_code == 200
        assert b'Payments' in response.data
        assert b'<table style="width:100%">' in response.data
        assert b'<h4>academy Payments</h4>' in response.data
        assert session['email'] == 'pz@email.com'
        assert session['user_id'] == 1
        assert b'2' in response.data # check code
        assert b'500' in response.data # check amount paid
        assert b'2022' in response.data # check date
        # assert b'sepi' in response.data # check student name
        # assert b'zed' in response.data # check lastname
        # assert b'300' in response.data # check tuition
        

def test_update_student(client, auth):
    """ Test the update route and functions"""
    pass

def test_remove_student(client, auth):
    """ Test the remove route and functions"""
    pass

def test_generate_report(client, auth):
    """ Tets the generate report route"""
    pass
