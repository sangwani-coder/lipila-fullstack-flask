from lipila import create_app


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


def test_index(client):
    response = client.get('/lipila/login')
    assert response.status_code == 200
    assert b"Log In" in response.data
    assert b"Register" in response.data