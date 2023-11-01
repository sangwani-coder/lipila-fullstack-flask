"""
    test_payment.py
    Lipila Fee Collection System
    Creator: Sangwani P. Zyambo

    unittests for views that handle payment.
"""
from db import get_db
from flask import g, session
from datetime import datetime
from lipila_app.helpers import get_payments


def test_payment_login_fail(client):
    """ test the pay route login
        with invalid code
    """
    with client:
        response = client.post(
            '/lipila/pay',
            data={
                'student':200
            }
        )
    assert b'Invalid code' in response.data

def test_payment_login_pass1(client):
    """ test the pay route login with
        existing student
    """
    with client:
        response = client.post(
            '/lipila/pay',
            data={
                'student':"PZ23002"
            }
        )
    assert response.headers['Location'] == '/lipila/payment/2'

def test_payment_login_pass2(client):
    """ test the pay route login with
        existing student
    """
    with client:
        response = client.post(
            '/lipila/pay',
            data={
                'student':"JZ23015"
            }
        )
    assert response.headers['Location'] == '/lipila/payment/15'


def test_get_student_data(client):
    """ Test the route to return student data"""

    with client:
        response = client.get('/lipila/payment/1')

        assert response.status_code == 200
        assert b'sepi' in response.data
        assert b'academy' in response.data

        # test session data
        assert session['user-id'] == 1
        assert session['firstname'] == 'sepi'
        assert session['lastname'] == 'zed'
        assert session['school'] == 'academy'
        assert session['tuition'] == 300

        # Start a new payment session
        response = client.get('/lipila/payment/3')
        assert response.status_code == 200
        assert b'mule' in response.data

        # test session data
        assert session['user-id'] == 3
        assert session['firstname'] == 'mule'
        assert session['lastname'] == 'mule'
        assert session['school'] == 'academy'
        assert session['tuition'] == 300

        # Create new sessions with different id
        response = client.get('/lipila/payment/2')

        assert response.status_code == 200
        assert b'pita' in response.data
        assert b'academy' in response.data

        assert session['user-id'] == 2
        assert session['firstname'] == 'pita'
        assert session['lastname'] == 'zed'
        assert session['school'] == 'academy'
        assert session['tuition'] == 300


def test_get_student_data_validate_input(client):
    with client:
        response = client.get('/lipila/payment/5')
        assert response.status_code == 200

def test_payment_correct_mtn(client, app):
    """ test the payment route"""
    with client:
        res = client.get('/lipila/payment/1')
        assert res.status_code == 200
        assert session['user-id'] == 1

        assert client.get('/lipila/confirmed').status_code == 200
        response = client.post(
            '/lipila/confirmed',
            data={
                'amount':200,
                'mobile':'0969620939'
            }
        )
        assert session['account'] == '0969620939'
    
        assert client.get('/lipila/payment').status_code == 200
        assert session['net'] == 'mtn'
        res = client.post('/lipila/payment')
        assert res.headers['Location'] == '/lipila/history'
    
    with client:
        response = client.post('/lipila/payment')
        assert response.headers['Location'] == '/lipila/history'
        with app.app_context():
            payment  = get_payments(1)
            assert payment[0][5] == 500
            assert payment[2][5] == 600
            assert session['account'] == '0969620939'
            assert session['amount'] == 200
            assert isinstance(payment, list)

def test_payment_wrong_details(client, app):
    """ test the payment route"""
    with client:
        res = client.get('/lipila/payment/2')
        assert res.status_code == 200
        assert session['user-id'] == 2

        mobile = '0959620939'
        assert client.get('/lipila/confirmed').status_code == 200
        response = client.post(
            '/lipila/confirmed',
            data={
                'amount':200,
                'mobile': mobile
            }
        )
        assert session['account'] == 'None'
    
        assert client.get('/lipila/payment').status_code == 200
        assert session['net'] == None
        res = client.post('/lipila/payment')
        assert res.headers['Location'] == '/lipila/history'
    
    with client:
        response = client.post('/lipila/payment')
        assert response.headers['Location'] == '/lipila/history'
        # assert b'error' in response.data
        with app.app_context():
            conn = get_db()
            db = conn.cursor()
            db.execute(
                "SELECT * FROM payment WHERE student_id = '2'",
            )
            payment = db.fetchone()
            assert payment[5] == 500
            assert session['account'] == 'None'
            assert session['amount'] == 200

    
def test_payment_correct_airtel(client, app):
    """ test the payment route"""
    with client:
        res = client.get('/lipila/payment/2')
        assert res.status_code == 200
        assert session['user-id'] == 2

        assert client.get('/lipila/confirmed').status_code == 200
        response = client.post(
            '/lipila/confirmed',
            data={
                'amount':400,
                'mobile':'0971893155'
            }
        )
        assert session['account'] == '0971893155'
    
        assert client.get('/lipila/payment').status_code == 200
        assert session['net'] == 'airtel'
    
    with client:
        response = client.post('/lipila/payment')
        assert response.headers['Location'] == '/lipila/history'
        with app.app_context():
            payment = get_payments(2)
            assert payment is not None
            assert payment[6][2] == 'pita'
            assert payment[6][3] == 'zed'
            assert payment[6][5] == 400
            assert session['account'] == '0971893155'
            assert isinstance(payment[0][4], datetime)