import os

from flask import Flask, render_template


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'lipila.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
        if not os.environ.get("SUB_KEY"):
            raise RuntimeError("SUB_KEY not set")
    except OSError:
        pass


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

    return app