"""
    Test the skoolpay views
    Auth: Peter S. Zyambo
"""

def test_homepage_get(client):
    response = client.get('/skoolpay/')
    assert response.status_code == 200
    assert b"<h4>Make a payment</h4>" in response.data
    assert b"<h1>Welcome to SkooPay</h1>" in response.data


def test_download(client):
    response = client.get('/skoolpay/download/1')
    assert response.status_code == 200
    assert b'receipt no# 1' in response.data

    response = client.get('/skoolpay/download/2')
    assert response.status_code == 200
    assert b'receipt no# 2' in response.data
    assert b'download' in response.data

    with client:
        response = client.get('/skoolpay/download/1')
        assert response.status_code == 200
    

