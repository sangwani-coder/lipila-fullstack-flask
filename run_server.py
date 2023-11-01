from lipila_app import app, db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from lipila_app.models.school import Schools
from lipila_app.models.user import User, Administrators, Parents
from lipila_app.models.student import Students
from flask import render_template

from lipila_app.views import auth
from lipila_app.views import lipila
from lipila_app.views import site_admin

# register blueprints
app.register_blueprint(auth.bp)
app.register_blueprint(lipila.bp)
# app.register_blueprint(admin.bp)
app.register_blueprint(site_admin.bp)

@app.route('/')
def index():
    # session.clear()
    return render_template('homepage.html')

if __name__ == '__main__':
    # Create admin
    admin = Admin(app, name='Lipila', template_mode='bootstrap3')

    #Add views
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Schools, db.session))
    admin.add_view(ModelView(Administrators, db.session))
    admin.add_view(ModelView(Parents, db.session))
    admin.add_view(ModelView(Students, db.session))
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)