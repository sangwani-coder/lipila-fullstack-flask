"""
    test_lipila.py
    Lipila Fee Collection System
    Creator: Sangwani P. Zyambo

    unittests for the lipila views.
"""
from flask import session

def test_landing_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Collect Fees Online From Students" in response.data

def test_download(client):
    response = client.get('/lipila/download/1')
    assert response.status_code == 200
    assert b'receipt no# 1' in response.data

    response = client.get('/lipila/download/2')
    assert response.status_code == 200
    assert b'receipt no# 2' in response.data
    assert b'download' in response.data

    with client:
        response = client.get('/lipila/download/1')
        assert response.status_code == 200
    
def test_set_student_session(client):
    with client:
        response = client.get('/lipila/payment/1')
        assert response.status_code == 200
        assert session['user-id'] == 1
        assert session['school'] == 'academy'
        assert session['school-id'] == 1

        response = client.get('/lipila/payment/7')
        assert response.status_code == 200
        assert session['user-id'] == 7
        assert session['school'] == 'switch academy'
        assert session['school-id'] == 2
        

def test_list_payments(client):
    """ Test ths route to return registered students"""
    with client:
        client.get('/lipila/payment/1')
        assert session['student'] == 'sepi zed'
        assert session['user-id'] == 1
        assert client.get('/lipila/confirmed').status_code == 200
        response = client.post(
            '/lipila/confirmed',
            data={
                'amount':400,
                'mobile':'0971893155'
            }
        )
        assert client.get('/lipila/payment').status_code == 200
        assert session['net'] == 'airtel'
        response = client.post('/lipila/payment')
        response = client.get('/lipila/history')
        assert response.status_code == 200
        assert b'Payments' in response.data
        assert b'academy Payments' in response.data
        assert b'sepi zed' in response.data

def test_confirmed(client):
    """ Test the route to return student data"""
    response = client.get('/lipila/payment/1')
    assert response.status_code == 200
    assert b'Enter amount:' in response.data
    assert b'Enter momo number:' in response.data

    with client:
        response = client.get('/lipila/confirmed')
        assert response.status_code == 200
        assert b'Confirmation' in response.data
        assert b'sepi' in response.data
        assert b'zed' in response.data
        assert b'academy' in response.data

        response = client.post(
            '/lipila/confirmed',
            data={
                'amount':200,
                'mobile':'0969620939'
            }
        )
        assert response.headers['Location'] == '/lipila/payment'

def test_pay(client):
    """ tests the GET request for the selection view function"""
    assert client.get('lipila/pay').status_code == 200
    with client:
        response = client.post(
            '/lipila/pay',
             data={
                'school':3
                }
            )
        assert response.status_code == 200