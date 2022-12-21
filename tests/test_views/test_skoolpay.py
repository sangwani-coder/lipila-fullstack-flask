"""
    Test the skoolpay views
    Auth: Peter S. Zyambo
"""
from skoolpay.db import get_db
from flask import g, session


def test_homepage_get(client):
    response = client.get('/skoolpay/')
    assert response.status_code == 200
    assert b"<h4>Make a payment</h4>" in response.data
    assert b"<h1>Welcome to SkooPay</h1>" in response.data

# def test_homepage_post(client):
#     response = client.post(
#         '/skoolpay',
#         data={'student':'1'}
#         )
#     assert response.status_code == 200
#     # assert response.headers['Location'] == '/skoolpay/payment/1'
#     assert b'sepi' in response.data
#     assert b'academy' in response.data
    

