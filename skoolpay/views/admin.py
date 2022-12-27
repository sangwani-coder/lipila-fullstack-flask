from .auth import login_required
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from skoolpay.db import get_db
import datetime as DT

from skoolpay.helpers import calculate_amount, calculate_payments, show_recent

bp = Blueprint('admin', __name__, url_prefix='/skoolpay')


@bp.route('/admin/dashboard', methods=('GET', 'POST'))
@login_required
def dashboard():
    db = get_db()
    this_month = (DT.date(DT.date.today().isocalendar()[0], 1, 1))
    this_week = (DT.date(DT.date.today().isocalendar()[0], 1, 1))
    this_day = (DT.date(DT.date.today().isocalendar()[0], 1, 1))

    data = show_recent(session['user_id'])
    # select year payments
    data_all = calculate_payments('all', session['user_id'])
    amount_all = calculate_amount('all', session['user_id'])

    # select month payments
    data_month = calculate_payments('month', session['user_id'])
    amount_month = calculate_amount('month', session['user_id'])

    #select week payments
    data_week = calculate_payments('week', session['user_id'])
    amount_week = calculate_amount('week', session['user_id'])

    #select day payments
    data_day = calculate_payments('day', session['user_id'])
    amount_day = calculate_amount('day', session['user_id'])
    
    payments = {'year':data_all, 'month':data_month, 'week':data_week, 'day':data_day}
    total = {'year':amount_all, 'month':amount_month, 'week':amount_week, 'day':amount_day}
    return render_template('admin/dashboard.html', data=data, total=total, payments=payments)

@bp.route('/admin/students', methods=('GET', 'POST'))
@login_required
def show_students():
    db = get_db()
    if request.method == 'GET':
        try:
            students = db.execute(
                "SELECT * from student WHERE school=?",(session['user_id'],)
            ).fetchall()
            return render_template('school/student.html', students=students)

        except Exception as e:
            print(e)

@bp.route('/admin/payments', methods=('GET', 'POST'))
@login_required
def show_payments():
    db = get_db()

    if request.method == 'GET':
        school = db.execute(
            "SELECT * from school WHERE id=?",(session['user_id'],)
        ).fetchone()

        id = str(school['id'])
        payment = db.execute(
                "SELECT * FROM payment WHERE school=?",(id,)
            ).fetchall()
        
        return render_template('school/payments.html', school=school['school'], data=payment)
    

@bp.route('/admin/add', methods = ['GET', 'POST'])
@login_required
def create_student():
    if request.method == 'POST':
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        school = session['user_id']
        tuition = request.form.get('tuition')
        program = 'nursing'

        db = get_db()
        error = None

        if not firstname:
            error = "firstname is required"
        elif  not lastname:
            error = "lastname is required"
        elif not tuition:
            error = 'tuition is required'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO student (firstname, lastname, school, program,\
                         tuition)\
                             VALUES (?, ?, ?, ?, ?)",
                    (firstname, lastname, school, program, tuition),
                )
                db.commit()
            except db.IntegrityError:
                error = "already registered."
            else:
                flash('student added successfully. Add another')
                return redirect(url_for('admin.create_student'))

        flash(error)
    return render_template('school/create.html')


@bp.route('/admin/update/<id>', methods = ['GET', 'POST'])
@login_required
def update_student(id):
    return render_template('school/update.html')


@bp.route('/admin/remove/<id>', methods = ['GET', 'POST'])
@login_required
def remove_student(id):
    return render_template('school/remove.html')


@bp.route('/admin/report', methods = ['GET', 'POST'])
@login_required
def report_student():
    return render_template('school/report.html')