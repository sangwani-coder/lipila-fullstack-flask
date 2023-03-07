"""
    helpers.py
    Lipila Fee Collection System
    Creator: Sangwani P. Zyambo

    defines view functions for the school admin.
"""
import os
from .auth import login_required
from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for,
    current_app, send_from_directory
)
from lipila.helpers import (
    get_student, get_user, send_email, search_email,
    generate_pay_code
    )

from lipila.db import get_db
import datetime as DT
from werkzeug.utils import secure_filename

from lipila.helpers import (
    calculate_amount, upload_excel_file,
    show_recent, allowed_file, get_number_of_students,
    add_uploaded_data
    )
from werkzeug.security import generate_password_hash
import csv

bp = Blueprint('admin', __name__, url_prefix='/lipila')


@bp.route('/admin/dashboard', methods=('GET', 'POST'))
@login_required
def dashboard():
    """
        School admin dashboard route
    """    
    data = show_recent(session['user_id'])
    # select the whole years payments
    data_all = calculate_amount('all', session['user_id'])

    # select current month payments
    data_month = calculate_amount('month', session['user_id'])

    #select current week payments
    data_week = calculate_amount('week', session['user_id'])

    #select todays payments
    data_day = calculate_amount('day', session['user_id'])
    
    total_amount_paid = {
        'year':data_all[0],
        'month':data_month[0],
        'week':data_week[0],
        'day':data_day[0]
        }
    total_payments = {
        'year':data_all[1],
        'month':data_month[1],
        'week':data_week[1],
        'day':data_day[1]
        }

    return render_template('admin/dashboard.html',
                           data=data, total=total_amount_paid,
                           payments=total_payments)

@bp.route('/admin/students', methods=('GET', 'POST'))
@login_required
def show_students():
    conn = get_db()
    db = conn.cursor()
    if request.method == 'GET':
        db.execute(
            "SELECT * from student WHERE school=%s",(session['user_id'],)
        )
        students = db.fetchall()
    return render_template('school/student.html', students=students)

@bp.route('/admin/payments', methods=('GET', 'POST'))
@login_required
def show_payments():
    conn = get_db()
    db = conn.cursor()

    if request.method == 'GET':
        db.execute(
            "SELECT * from school WHERE id=%s",(session['user_id'],)
        )
        school = db.fetchone()

        id = str(school[0])
        db.execute(
                "SELECT * FROM payment WHERE school=%s",(id,)
            )
        payment = db.fetchall()
        
        return render_template('school/payments.html', school=school[3], data=payment)
    

@bp.route('/admin/add', methods = ['GET', 'POST'])
@login_required
def create_student():
    if request.method == 'POST':
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        school = session['user_id']
        tuition = request.form.get('tuition')
        program = request.form.get('program')
        
        conn = get_db()
        db = conn.cursor()
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
                             VALUES (%s, %s, %s, %s, %s) RETURNING id",
                    (firstname, lastname, school, program, tuition),
                )
                r_id = db.fetchone()[0]
                conn.commit()
                payment_code = generate_pay_code(firstname, lastname, r_id)
                
                db.execute(
                    "UPDATE student SET payment_code=%s" 'WHERE id=%s', (payment_code, r_id),
                )
                conn.commit()

            except Exception as e:
                error = "an error occured!"
            else:
                flash('student added successfully. Add another')
                return redirect(url_for('admin.create_student'))

        flash(error)
    return render_template('school/create.html')

# Update view
@bp.route('/admin/update/<int:id>', methods = ['GET', 'POST'])
@login_required
def update(id):
    """
        Updates a students information
    """
    student = get_student(id)

    if request.method == 'POST':
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        school = session['user_id']
        tuition = request.form.get('tuition')
        program = request.form.get('program')

        conn = get_db()
        db = conn.cursor()
        error = None

        if not firstname:
            error = "firstname is required"
        elif  not lastname:
            error = "lastname is required"
        elif not tuition:
            error = 'tuition is required'

        if error is not None:
            flash(error)
        else:
            db.execute(
                "UPDATE student SET firstname = %s,\
                    lastname = %s, school = %s, program = %s,\
                        tuition = %s" 'WHERE id = %s',
                        (firstname, lastname, school, program, tuition,id),
                )
            conn.commit()
            flash('Student Updated Successfully')
            return redirect(url_for('admin.show_students'))

    return render_template('school/update.html', student=student)

# Delete view
@bp.route('/delete/<int:id>', methods=('POST',))
@login_required
def delete(id):
    get_student(id)
    conn = get_db()
    db = conn.cursor()
    db.execute('DELETE FROM student WHERE id = %s', (id,))
    conn.commit()
    flash('Student Deleted Successfully')
    return redirect(url_for('admin.show_students'))

@bp.route('/admin/resetpassword', methods = ['GET', 'POST'])
def reset_password():
    """
        returns a from for the user to confirm registration
    """
    if request.method == 'POST':
        error = None
        email = request.form.get('email')
        if not email:
            error = "Email is required"
        if not error:
            user = search_email(email)
            if user is not None:
                body = "You requested to reset your email"
                msg = "Check your email for a link to reset your password"
                send_email(email, 'Password Reset', body, msg, )
            else:
                flash("User not found!")
            return redirect(url_for('landing'))
    return render_template('admin/reset.html')


# Update admin password view
@bp.route('/admin/changepassword/<int:id>', methods = ['GET', 'POST'])
@login_required
def update_password(id):
    """
        Resets the users password
    """

    if request.method == 'POST':
        password = request.form.get('password')

        conn = get_db()
        db = conn.cursor()
        error = None

        if not password:
            error = "password is required"
    
        if error is not None:
            flash(error)
        else:
            db.execute(
                "UPDATE school SET password = %s" 'WHERE id = %s',
                        (generate_password_hash(password),id),
                )
            conn.commit()
            flash('Password Changed Successfully')
            return redirect(url_for('landing'))
    return render_template('admin/reset_password.html')


@bp.route('/admin/profile', methods = ['GET', 'POST'])
@login_required
def profile():
    """View to edit the users profile"""
    id = session['user_id']
    if request.method == 'POST':
        email = request.form['email']
        mobile = request.form['mobile']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
    
        error = None        
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
        elif not email:
            error = 'Firstname is required.'
        elif not reg_number:
            error = 'Registration number is required.'
        elif not job:
            error = 'Job description is required.'

        if error is None:
            conn = get_db()
            db = conn.cursor()
            db.execute(
                "UPDATE school SET job=%s, school=%s, email=%s, mobile=%s,\
                        reg_number=%s, firstname=%s, lastname=%s" 'WHERE id=%s',
                        (job, school, email, mobile, reg_number, firstname,
                lastname, id),
            )
            conn.commit()
            
            msg = "Profile Updated"
            flash(msg)
            session['school'] = school
            user = get_user(id)
            return render_template('admin/profile.html', user=user)

        flash(error)
    user = get_user(id)
    return render_template('admin/profile.html', user=user)

@bp.route('/admin/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    """ uploads a cvs/xlsx file with student data
    """
    error = None
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            
            basedir = os.path.abspath(os.path.dirname(__file__))
            file.save(os.path.join(basedir, current_app.config['UPLOAD_FOLDER'], filename))
            data = upload_excel_file('/home/pita/lipila/lipila/views/static/uploads/students.xlsx')
            msg = add_uploaded_data(data)
            if msg == 'students added successfully.':
                flash(msg)
                return redirect(url_for('admin.show_students')), 201
        return redirect(request.url)

    return render_template('school/upload.html')