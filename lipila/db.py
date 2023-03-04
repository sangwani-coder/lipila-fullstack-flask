"""
    db.py
    Lipila Fee Collection System
    Creator: Sangwani P. Zyambo

    Module that defines funcitons for datbase initialization and connection.
"""
import click
from flask import current_app, g
import os
import psycopg2


def get_db():
    if 'db' not in g:
        if os.environ.get('LIP_ENV') == "db":
            conn = psycopg2.connect(
                host=os.environ.get('PGHOST'),
                database=os.environ.get('PGDATABASE'),
                user=os.environ.get('PGUSER'),
                password=os.environ.get('PGPASSWORD'))
            g.db = conn

        else:
            conn = psycopg2.connect(
                host=os.environ.get('PGHOST'),
                database=os.environ.get('TESTDATABASE'),
                user=os.environ.get('PGUSER'),
                password=os.environ.get('PGPASSWORD'))
            g.db = conn

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    conn = get_db()
    db = conn.cursor()
    if os.environ.get('PGDATABASE') == "lipila":
        with current_app.open_resource("schema-pro.sql") as f:
            db.execute(f.read().decode('utf8'))

    elif os.environ.get('PGDATABASE') != 'postgres':
        with current_app.open_resource('schema.sql') as f:
            db.executescript(f.read().decode('utf8'))
    conn.commit()

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)