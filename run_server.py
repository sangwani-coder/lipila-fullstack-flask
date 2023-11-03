from lipila_app import app, db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from lipila_app.models.school import (
    School, Administrator, Parents,
    SchoolFees, Students, OtherFees, Payments,
)
from lipila_app.models.user import User, MyAdminIndexView, MyModelView, init_login, build_sample_db
from flask import render_template

from lipila_app.views import lipila
from lipila_app.views import site_admin

# register blueprints
app.register_blueprint(lipila.bp)
app.register_blueprint(site_admin.bp)


@app.route('/')
def index():
    # session.clear()
    return render_template('index.html')


if __name__ == '__main__':
    # Lipila Admin views
    # Initialize flask-login
    init_login()

    # Create admin
    admin = Admin(app, name='Lipila', index_view=MyAdminIndexView(), base_template='layout.html', template_mode='bootstrap4')

    # Add view
    admin.add_view(MyModelView(User, db.session))

    # admin = Admin(app, name='Lipila', template_mode='bootstrap3')
    # admin.add_view(ModelView(User, db.session))
    admin.add_view(MyModelView(School, db.session))
    admin.add_view(MyModelView(Administrator, db.session))

    
    admin.add_view(MyModelView(Parents, db.session))
    admin.add_view(ModelView(Students, db.session))
    admin.add_view(MyModelView(SchoolFees, db.session))
    admin.add_view(MyModelView(OtherFees, db.session))
    admin.add_view(MyModelView(Payments, db.session))

    with app.app_context():
        db.create_all()
        build_sample_db()

    app.run(debug=True)
