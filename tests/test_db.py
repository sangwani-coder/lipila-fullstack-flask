"""
    test_db.py
    Lipila Fee Collection System
    Creator: Sangwani P. Zyambo

    unittests for the db views.
"""
import pytest
from lipila_app.db import get_db
import psycopg2


def test_get_close_db(app):
    with app.app_context():
        conn = get_db()
        db = conn.cursor()
        assert isinstance(conn, type(get_db()))

    with pytest.raises(psycopg2.InterfaceError) as e:
        db.execute('SELECT 1')
        assert 'cursor already closed' in str(e.value)

def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('lipila.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Initialized' in result.output
    assert Recorder.called