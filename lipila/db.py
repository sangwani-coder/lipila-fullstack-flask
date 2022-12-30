import sqlite3

import click
from flask import current_app, g
import os
import psycopg2


def get_db():
    if 'db' not in g:
        if os.environ.get('PGDATABASE') == "postgres":
            conn = psycopg2.connect(
                host=os.environ.get('PGHOST'),
                database=os.environ.get('PGDATABASE'),
                user=os.environ['PGUSER'],
                password=os.environ['PGPASSWORD'])
            g.db = conn

        else:
            g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
            g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    conn = get_db()
    db = conn.cursor()
    if os.environ.get('PGDATABASE') == "postgres":
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