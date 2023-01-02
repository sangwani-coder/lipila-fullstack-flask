"""Test the side_admin views"""

def test_about(client):
    response = client.get('/lipila/about')
    assert response.status_code == 200
    assert b"Under Construction" in response.data

def test_contact(client):
    response = client.get('/lipila/contact')
    assert response.status_code == 200
    assert b"Contact" in response.data

def test_privacy(client):
    response = client.get('/lipila/privacy-policy')
    assert response.status_code == 200
    assert b"Under Construction" in response.data

def test_terms(client):
    response = client.get('/lipila/terms-conditions')
    assert response.status_code == 200
    assert b"Under Construction" in response.data

def test_faqs(client):
    response = client.get('/lipila/faqs')
    assert response.status_code == 200
    assert b"Under Construction" in response.data

def test_features(client):
    response = client.get('/lipila/features')
    assert response.status_code == 200
    assert b"Online School Fees Payment" in response.data


def test_profile(client):
    response = client.get('/lipila/profile')
    assert response.status_code == 200
    assert b"Edit Profile" in response.data