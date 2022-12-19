from skoolpay import create_app


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


def test_index(client):
    response = client.get('/skoolpay/login')
    assert response.status_code == 200
    assert b'<h1>Welcome to SkooPay</h1>' in response.data
    assert b"Log In" in response.data
    assert b"Register" in response.data

    # auth.login()
    # response = client.get('/skoolpay')
    # assert b'Log Out' in response.data