"""
    Test the lipila views
    Auth: Peter S. Zyambo
"""

def test_homepage_get(client):
    response = client.get('/lipila/')
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
    

