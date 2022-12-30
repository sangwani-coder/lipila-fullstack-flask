"""
    Test the payment views
    Auth: Peter S. Zyambo
"""
import pytest
from lipila.db import get_db
from flask import g, session
from datetime import datetime

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
        assert b'sangwa' in response.data
        assert b'a' in response.data

        # test session data
        assert session['user-id'] == 3
        assert session['firstname'] == 'sangwa'
        assert session['lastname'] == 'zed'
        assert session['school'] == 'a'
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
        response = client.get('/lipila/payment/5')
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
            conn = get_db()
            db = conn.cursor()
            db.execute(
                "SELECT * FROM payment WHERE student_id = '1'",
            )
            payment = db.fetchone()
            assert payment is not None
            assert payment[3] == 500
            assert payment[1] == 1
            assert payment[5] == 1
            assert session['account'] == '0969620939'
            assert session['amount'] == 200
            assert isinstance(payment[2], datetime)

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
            assert payment[3] == 500
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
        res = client.post('/lipila/payment')
    
    with client:
        response = client.post('/lipila/payment')
        assert response.headers['Location'] == '/lipila/history'
        # assert b'success payment of 500 for sepi zed' in response.data
        with app.app_context():
            conn = get_db()
            db = conn.cursor()
            db.execute(
                "SELECT * FROM payment WHERE student_id = '2'",
            )
            payment = db.fetchone()
            assert payment is not None
            assert payment[3] != 400
            assert payment[1] == 2
            assert payment[5] == 2
            assert session['account'] == '0971893155'
            assert session['amount'] == 400
            assert isinstance(payment[2], datetime)