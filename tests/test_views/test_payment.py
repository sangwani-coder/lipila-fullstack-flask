"""
    test_payment.py
    Lipila Fee Collection System
    Creator: Sangwani P. Zyambo

    unittests for views that handle payment.
"""
from lipila.db import get_db
from flask import g, session
from datetime import datetime
from lipila.helpers import get_payments
import pytest

def test_set_student_session(client):
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


def test_get__student_data_validate_input(client):
    with client:
        response = client.get('/lipila/payment/20')
        assert response.status_code == 200
        assert b'No student found!' in response.data

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

def test_selection_get(client, app):
    """ tests the GET request for the selection view function"""
    with client:
        with app.app_context():
            response = client.post(
                '/lipila/pay',
                data={
                    'school':'7',
                    }
                )
            assert response.status_code == 200
            response = client.get('/lipila/selection')
            assert response.status_code == 200
            assert b'tuition' in response.data
            assert b'transport' in response.data
            assert b'extra' in response.data
            assert b'uniform' in response.data
            assert session['std'] == 7

def test_selection_post(client, app):
    """ tests the POST request for the selection view function"""
    with client:
        assert client.post('/lipila/pay', data={'school':9}).status_code == 200
        response = client.post('/lipila/selection',
                data = {
                    'tuition':'tuition', 'transport':'transport', 
                    'extra-lessons':'extra-lessons', 'uniform':'uniform'
                    }
                )
        assert response.headers['Location'] == '/lipila/confirmed'
        with app.app_context():
            assert session['tuition'] == 'tuition'
            assert session['transport'] == 'transport'
            assert session['extra'] == 'extra-lessons'
            assert session['uniform'] == 'uniform'

        # test 2 choices
        assert client.post('/lipila/pay', data = {'school':7}).status_code == 200
        response = client.post('/lipila/selection',
                data = {
                    'tuition':'tuition', 'transport':'transport'
                    }
                )
        assert response.headers['Location'] == '/lipila/confirmed'
        with app.app_context():
            assert session['tuition'] == 'tuition'
            assert session['transport'] == 'transport'

        with pytest.raises(KeyError) as e:
            session['extra']
            session['uniform']