"""
    __init__.py
    Lipila Fee Collection System
    Creator: Sangwani P. Zyambo

    The application factory.
"""
import os
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy

from flask import Flask, session, render_template
from models.school import School
import datetime

from views import auth
from views import admin
from views import lipila
from views import site_admin


UPLOAD_FOLDER = '/files/uploads'

# create and configure the app
app = Flask(__name__, instance_relative_config=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.secret_key = "my_secret_key"

database=os.environ.get('PGDATABASE')
user=os.environ.get('PGUSER')
password=os.environ.get('PGPASSWORD')
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://%s:%s@localhost:5432/lipiladb" %(user, password)


db = SQLAlchemy(app)
# db.init_app(app)

# set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

admin = Admin(app, name='microblog', template_mode='bootstrap3')


# register blueprints
app.register_blueprint(auth.bp)
app.register_blueprint(lipila.bp)
# app.register_blueprint(admin.bp)
app.register_blueprint(site_admin.bp)

# if test_config is None:
#     if not os.environ.get("SUB_KEY"):
#         raise RuntimeError("SUB_KEY not set")
#     if not os.environ.get("MAIL_PASSWORD"):
#         raise RuntimeError("MAIL_PASSWORD not set")

# else:
#     # load the test config if passed in
#     app.config.from_mapping(test_config)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(64))
    email = db.Column(db.Unicode(64))
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)

    def __unicode__(self):
        return self.name
    
# Flask and Flask-SQLAlchemy initialization here
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(School, db.session))

@app.route('/', methods = ['GET', 'POST'])
def landing():
    session.clear()
    return render_template('homepage.html')


@app.route('/lipila/<task>', methods = ['GET', 'POST'])
def index(task):
    # return "Index"
    return render_template('index.html')


# # rgister init_app
# from lipila import db
# db.init_app(app)

if __name__ == '__main__':

    # Build a sample db on the fly, if one does not exist yet.
    # app_dir = os.realpath(os.path.dirname(__file__))
    # database_path = os.join(app_dir, app.config['DATABASE_FILE'])
    # if not os.path.exists(database_path):
    #     with app.app_context():
    #         build_sample_db()

    # Start app
    
    
    app.run(debug=True)