import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

UPLOAD_FOLDER = '/files/uploads'
FLASK_ADMIN_SWATCH = 'cerulean'

# create and configure the app
UPLOAD_FOLDER = UPLOAD_FOLDER
MAIL_SERVER='smtp.gmail.com'
MAIL_PORT = 465
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
MAIL_USE_TLS = False
MAIL_USE_SSL = True
SECRET_KEY = "my_secret_key"

# set database user
database=os.environ.get('PGDATABASE')
user=os.environ.get('PGUSER')
password=os.environ.get('PGPASSWORD')

SQLALCHEMY_DATABASE_URI = "postgresql://%s:%s@localhost:5432/lipiladb" %(user, password)
SQLALCHEMY_ECHO = True