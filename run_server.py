from lipila_app import app, db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from lipila_app.models.school import (
    School, Administrator, Parents,
    SchoolFees, Students, OtherFees, Payments,
)
from lipila_app.models.user import User
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
    admin = Admin(app, name='Lipila', template_mode='bootstrap3')
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(School, db.session))
    admin.add_view(ModelView(Administrator, db.session))

    # school admin views
    schooladmin = Admin(app, name='School', url="/schooladmin",
                   endpoint="schooladmin", template_mode='babel')
    schooladmin.add_view(ModelView(Parents, db.session))
    schooladmin.add_view(ModelView(Students, db.session))
    schooladmin.add_view(ModelView(SchoolFees, db.session))
    schooladmin.add_view(ModelView(OtherFees, db.session))
    schooladmin.add_view(ModelView(Payments, db.session))

    with app.app_context():
        db.create_all()

    app.run(debug=True)
