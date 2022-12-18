import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from .db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register/<user>', methods=('GET', 'POST'))
def register(user):
    if request.method == 'POST':
        email = request.form['email']
        mobile = request.form['mobile']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        password = request.form['password']
    
        db = get_db()
        error = None

        if user == 'users':
            if not email:
                error = 'Email is required.'
            elif not mobile:
                error = 'Mobile is required.'
            elif not firstname:
                error = 'Firstname is required.'
            elif not lastname:
                error = 'Lastname is required.'
            elif not password:
                error = 'Password is required.'
            
        if user == 'schools':
            # admin other detaild
            user_status = request.form['job']
            school = request.form['school']
            reg_number = request.form['reg_number']

            if not school:
                error = 'School is required.'
            elif not mobile:
                error = 'Mobile is required.'
            elif not firstname:
                error = 'Firstname is required.'
            elif not lastname:
                error = 'Lastname is required.'
            elif not password:
                error = 'Password is required.'
            elif not email:
                error = 'Firstname is required.'
            elif not reg_number:
                error = 'Registration number is required.'
            elif not user_status:
                error = 'Job description is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (email, password) VALUES (?, ?)",
                    (email, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {email} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    if user == 'users':
        return render_template('auth/register_user.html')
    else:
        return render_template('auth/register_school.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        users = request.method.get('user')
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE email = ?', (email,)
        ).fetchone()

        if user is None:
            error = 'Incorrect email.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('dashboard', user=users))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view