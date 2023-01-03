"""
    test_factory.py
    Lipila Fee Collection System
    Creator: Sangwani P. Zyambo

    unittests for the app factory(__init__.py) views.
"""

from lipila import create_app


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing

def test_index(client):
    response = client.get('/lipila/login')
    assert response.status_code == 200