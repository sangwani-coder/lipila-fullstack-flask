"""
    Test the admin view
    Auth: Peter S. Zyambo
"""
import pytest
from lipila.db import get_db
from flask import g, session


def test_dashboard(client, auth):
    response = auth.login()
    assert response.headers["Location"] == "/lipila/admin/dashboard"

    with client:
        res = client.get('/lipila/admin/dashboard')
        assert session['user_id'] == 1
        assert session['email'] == 'zyambo@icloud.com'
        assert b'academy' in res.data

def test_create_student(client, auth, app):
    """ test the add_student route and methods"""
    response = auth.login()
    assert response.headers['Location'] == '/lipila/admin/dashboard'
    with client:
        assert client.get('/lipila/admin/add').status_code == 200

    response = client.post(
        '/lipila/admin/add', data={
            'firstname':'ab', 'lastname':'b', 'school':1,
            'program':'b', 'tuition':300,
            }
    )
    assert response.headers['Location'] == '/lipila/admin/add'

    with app.app_context():
        conn = get_db()
        db = conn.cursor()
        db.execute(
            "SELECT * FROM student WHERE firstname = 'ab'",
        )
        assert db.fetchone() is not None


@pytest.mark.parametrize((
    'firstname', 'lastname', 'school', 'program', 'tuition', 'message'), (
    ('', '','','','', b'firstname is required'),
    ('p', '','','','', b'lastname is required'),
    ('p', 'z',1,'se','', b'tuition is required'),
))
def test_create_student_validate_input(
    client, auth, firstname, lastname, school, program, tuition, message):
    response = auth.login()
    assert response.headers['Location'] == '/lipila/admin/dashboard'
    with client:
        assert client.get('/lipila/admin/add').status_code == 200
    response = client.post(
        '/lipila/admin/add',
        data={
            'firstname':firstname, 'lastname':lastname, 'school':school,
            'program':program, 'tuition':tuition}
    )
    assert response.status_code == 200
    assert message in response.data

def test_show_students(client, auth):
    """ Test ths route to return registered students"""
    response = auth.login()
    assert response.headers['Location'] == '/lipila/admin/dashboard'
    with client:
        response = client.get('/lipila/admin/students')
        assert response.status_code == 200
        assert session['email'] == 'zyambo@icloud.com'
        assert b'pita' in response.data
        assert b'pita' in response.data
        assert b'sepi' in response.data
        assert b'sangwa' not in response.data
        assert b'zed' in response.data

def test_list_payments(client, auth):
    """ Test the route to return registered students"""
    response = auth.login()
    assert response.headers['Location'] == '/lipila/admin/dashboard'
    with client:
        response = client.get('/lipila/admin/payments')
        assert response.status_code == 200
        assert b'Payments' in response.data
        assert b'<h4>academy Payments</h4>' in response.data
        assert session['email'] == 'zyambo@icloud.com'
        assert session['user_id'] == 1
        assert b'2' in response.data # check code
        assert b'500' in response.data # check amount paid
        assert b'2023' in response.data # check date


def test_update_get(client, auth):
    """ Test the update view"""
    response = auth.login()
    assert response.headers['Location'] == '/lipila/admin/dashboard'
    with client:
        response = client.get('/lipila/admin/update/1')
        assert response.status_code == 200
        assert b'<h3>Update Student details</h3>' in response.data
        assert b'sepi' in response.data
        assert b'zed' in response.data
        assert b'IT' in response.data
        assert b'300' in response.data

def test_update_post(client, auth, app):
    """ test the add_student route and methods"""
    auth.login()

    response = client.post(
        '/lipila/admin/update/2', data={
            'firstname':'Sepiso', 'lastname':'Zyambo', 'school':1,
            'program':'Medicine', 'tuition':750,
            }
    )
    assert response.headers['Location'] == '/lipila/admin/students'
    # assert b'Student Updated Successfully' in response.data

    with app.app_context():
        conn = get_db()
        db = conn.cursor()
        db.execute(
            "SELECT * FROM student WHERE id=2",
        )
        data = db.fetchone()
        assert data is not None
        assert data[5] == 750
        assert data[1] == "Sepiso"
        assert data[4] == "Medicine"
    

# def test_delete(client, auth, app):
#     """ Test the delete view"""
#     response = auth.login()
#     assert response.headers['Location'] == '/lipila/admin/dashboard'
#     with client:
#         response = client.post('/lipila/admin/delete/1')
#         assert response.headers['Location'] == '/lipila/admin/dashboard'

#         with app.app_context():
#             conn = get_db()
#             db = conn.cursor()
#             db.execute(
#                 "SELECT * FROM student WHERE id=1",
#             )
#             data = db.fetchone()
#             assert data is None