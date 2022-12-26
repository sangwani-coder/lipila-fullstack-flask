"""
    Test the payment views
    Auth: Peter S. Zyambo
"""
import pytest
from skoolpay.db import get_db
from flask import g, session
from datetime import datetime

def test_get_student_data(client):
    """ Test the route to return student data"""

    with client:
        response = client.get('/skoolpay/payment/1')

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
        response = client.get('/skoolpay/payment/3')
        assert response.status_code == 200
        assert b'sangwa' in response.data
        assert b'a' in response.data

        # test session data
        assert session['user-id'] == 3
        assert session['firstname'] == 'sangwa'
        assert session['lastname'] == 'zed'
        assert session['school'] == 'a'
        assert session['tuition'] == 300

        # Create new sessions with different id
        response = client.get('/skoolpay/payment/2')

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
        response = client.get('/skoolpay/payment/5')
        assert response.status_code == 200
        assert b'No student found!' in response.data

def test_confirmed(client):
    """ Test the route to return student data"""
    response = client.get('/skoolpay/payment/1')
    assert response.status_code == 200
    assert b'Enter amount:' in response.data
    assert b'Enter momo number:' in response.data

    with client:
        response = client.get('/skoolpay/confirmed')
        assert response.status_code == 200
        assert b'Confirmation' in response.data
        assert b'sepi' in response.data
        assert b'zed' in response.data
        assert b'academy' in response.data

        response = client.post(
            '/skoolpay/confirmed',
            data={
                'amount':200,
                'mobile':'0969620939'
            }
        )
        assert response.headers['Location'] == '/skoolpay/payment'

def test_payment_correct_mtn(client, app):
    """ test the payment route"""
    with client:
        res = client.get('/skoolpay/payment/1')
        assert res.status_code == 200
        assert session['user-id'] == 1

        assert client.get('/skoolpay/confirmed').status_code == 200
        response = client.post(
            '/skoolpay/confirmed',
            data={
                'amount':200,
                'mobile':'0969620939'
            }
        )
        assert session['account'] == '0969620939'
    
        assert client.get('/skoolpay/payment').status_code == 200
        assert session['net'] == 'mtn'
        res = client.post('/skoolpay/payment')
        assert res.headers['Location'] == '/skoolpay/history'
    
    with client:
        response = client.post('/skoolpay/payment')
        assert response.headers['Location'] == '/skoolpay/history'
        # assert b'success payment of 500 for sepi zed' in response.data
        with app.app_context():
            payment = get_db().execute(
                "SELECT * FROM payment WHERE student_id = '1'",
            ).fetchone()
            assert payment is not None
            assert payment['amount'] == 500
            assert payment['student_id'] == 1
            assert payment['school'] == 1
            assert session['account'] == '0969620939'
            assert session['amount'] == 200
            assert isinstance(payment['created'], datetime)

def test_payment_wrong_details(client, app):
    """ test the payment route"""
    with client:
        res = client.get('/skoolpay/payment/2')
        assert res.status_code == 200
        assert session['user-id'] == 2

        mobile = '0959620939'
        assert client.get('/skoolpay/confirmed').status_code == 200
        response = client.post(
            '/skoolpay/confirmed',
            data={
                'amount':200,
                'mobile': mobile
            }
        )
        assert session['account'] == 'None'
    
        assert client.get('/skoolpay/payment').status_code == 200
        assert session['net'] == None
        res = client.post('/skoolpay/payment')
        assert res.headers['Location'] == '/skoolpay/history'
    
    with client:
        response = client.post('/skoolpay/payment')
        assert response.headers['Location'] == '/skoolpay/history'
        # assert b'error' in response.data
        with app.app_context():
            payment = get_db().execute(
                "SELECT * FROM payment WHERE student_id = '2'",
            ).fetchone()
            assert payment['amount'] == 500
            assert session['account'] == 'None'
            assert session['amount'] == 200

    
def test_payment_correct_airtel(client, app):
    """ test the payment route"""
    with client:
        res = client.get('/skoolpay/payment/2')
        assert res.status_code == 200
        assert session['user-id'] == 2

        assert client.get('/skoolpay/confirmed').status_code == 200
        response = client.post(
            '/skoolpay/confirmed',
            data={
                'amount':400,
                'mobile':'0971893155'
            }
        )
        assert session['account'] == '0971893155'
    
        assert client.get('/skoolpay/payment').status_code == 200
        assert session['net'] == 'airtel'
        res = client.post('/skoolpay/payment')
    
    with client:
        response = client.post('/skoolpay/payment')
        assert response.headers['Location'] == '/skoolpay/history'
        # assert b'success payment of 500 for sepi zed' in response.data
        with app.app_context():
            payment = get_db().execute(
                "SELECT * FROM payment WHERE student_id = '2'",
            ).fetchone()
            assert payment is not None
            assert payment['amount'] != 400
            assert payment['student_id'] == 2
            assert payment['school'] == 2
            assert session['account'] == '0971893155'
            assert session['amount'] == 400
            assert isinstance(payment['created'], datetime)