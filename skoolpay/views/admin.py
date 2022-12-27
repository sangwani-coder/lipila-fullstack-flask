from .auth import login_required
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from skoolpay.db import get_db

bp = Blueprint('admin', __name__, url_prefix='/skoolpay')


@bp.route('/admin/dashboard', methods=('GET', 'POST'))
@login_required
def dashboard():
    return render_template('admin/dashboard.html')

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