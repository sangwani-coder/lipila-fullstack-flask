from flask_sqlalchemy import SQLAlchemy
from flask import Flask


app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
