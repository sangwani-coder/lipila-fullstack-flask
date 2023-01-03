"""
    auth.py
    Lipila Fee Collection System
    Creator: Sangwani P. Zyambo

    Module that defines the authentication views.
"""
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from lipila.db import get_db
from lipila.helpers import send_email

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register/<user>', methods=('GET', 'POST'))
def register(user):
    if request.method == 'POST':
        email = request.form['email']
        mobile = request.form['mobile']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        password = request.form['password']
    
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
            job = request.form['job']
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
            elif not job:
                error = 'Job description is required.'

        if error is None:
            try:
                conn = get_db()
                db = conn.cursor()
                db.execute(
                    "INSERT INTO school (job, school, email, mobile,\
                         reg_number, firstname, lastname, password)\
                             VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (job, school, email, mobile, reg_number, firstname,
                    lastname, generate_password_hash(password)),
                )
                conn.commit()
                
                # send registration confirmation email
                email = email
                sub = 'Registration Success'
                body = '{} Welcome to Lipila Online Fee Collection System. Your \
                        username: {}' .format(school, email)
                subject = 'Registration Succesfull.'

                msg = send_email(email, sub, body, subject)
                flash(msg)

            except Exception as e:
                error = "already registered."
            else:
                return redirect(url_for("auth.login", users='schools'))

        flash(error)

    if user == 'users':
        return render_template('auth/register_user.html')
    else:
        return render_template('auth/register_school.html')


@bp.route('/login/<users>', methods=('GET', 'POST'))
def login(users):
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = get_db()
        db = conn.cursor()
        error = None
        # login student user
        if users == 'users':
            db.execute(
                'SELECT * FROM school WHERE email = %s', (email,)
            )
            user = db.fetchone()

            if user is None:
                error = 'Incorrect email.'
            elif not check_password_hash(user[8], password):
                error = 'Incorrect password.'

        # login admin user
        elif users == 'schools':
            db.execute(
                'SELECT * FROM school WHERE email = %s', (email,)
            )
            user = db.fetchone()
            if user is None or not check_password_hash(user[9], password):
                error = 'Incorrect credentials. Please check your details'

        if error is None:
            flash('Logged in')
            session['user'] = users
            session['user_id'] = user[0]
            session['email'] = user[4]
            session['school'] = user[3]
            return redirect(url_for('admin.dashboard'))

        flash(error)

    return render_template('index.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        conn = get_db()
        db = conn.cursor()
        db.execute(
            'SELECT * FROM school WHERE id = %s', (user_id,)
        )
        g.user = db.fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    flash('Logged out')
    return redirect(url_for('index', task='login'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash('Log in required')
            return redirect(url_for('auth.login', users='schools'))

        return view(**kwargs)

    return wrapped_view