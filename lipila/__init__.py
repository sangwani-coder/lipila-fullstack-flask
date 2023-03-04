"""
    __init__.py
    Lipila Fee Collection System
    Creator: Sangwani P. Zyambo

    The application factory.
"""
import os

from flask import Flask, render_template, session
UPLOAD_FOLDER = '/files/uploads'

def create_app(test_config=None):
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

    if test_config is None:
        if not os.environ.get("SUB_KEY"):
            raise RuntimeError("SUB_KEY not set")
        if not os.environ.get("MAIL_PASSWORD"):
            raise RuntimeError("MAIL_PASSWORD not set")

    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    @app.route('/', methods = ['GET', 'POST'])
    def landing():
        session.clear()
        return render_template('homepage.html')


    @app.route('/lipila/<task>', methods = ['GET', 'POST'])
    def index(task):
        # return "Index"
        return render_template('index.html')
    

    # rgister init_app
    from lipila import db
    db.init_app(app)
    
    # register auth blueprint
    from lipila.views import auth
    app.register_blueprint(auth.bp)

    # register lipila blueprint
    from lipila.views import lipila
    app.register_blueprint(lipila.bp)

    # register admin blueprint
    from lipila.views import admin
    app.register_blueprint(admin.bp)

    # register site admin blueprint
    from lipila.views import site_admin
    app.register_blueprint(site_admin.bp)

    return app