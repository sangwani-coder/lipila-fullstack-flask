from skoolpay.db import get_db
from flask import g, session


def test_homepage(client):
    response = client.get('/skoolpay/')
    assert response.status_code == 200
    assert b"<h3>Make a payment</h3>" in response.data
    assert b"<h1>Welcome to SkooPay</h1>" in response.data


def test_dashbord(client, auth):
    response = auth.login()
    assert response.headers["Location"] == "/skoolpay/dashboard"

    with client:
        res = client.get('/skoolpay/dashboard')
        assert session['user_id'] == 1
        assert g.user['email'] == 'pz@email.com'
        assert b'pz@email.com' in res.data
        assert b'Log Out' in res.data
        assert b'<h1>DASHBOARD</h1>' in res.data
