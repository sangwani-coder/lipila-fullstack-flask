import os
import tempfile

import pytest
from lipila import create_app
from lipila.db import get_db, init_db

from lipila.momo.momo import Momo

class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, email='zyambo@icloud.com', password='test'):
        return self._client.post(
            '/auth/login/schools',
            data={'email': email, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)


with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')

@pytest.fixture
def app():
    if os.environ.get('PGDATABASE') != "postgres":
        db_fd, db_path = tempfile.mkstemp()
        app = create_app({
            'TESTING': True,
            'DATABASE': db_path,
        })
    else:
        app = create_app({
            'TESTING': True,
            'DATABASE': os.environ.get('TESTDATABASE'),
        })

    with app.app_context():
        init_db()
        conn = get_db()
        db = conn.cursor()
        db.execute(_data_sql)
        conn.commit()

    yield app

    # os.close(db_fd)
    # os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def momo():
    return Momo()

