"""
    lipila.py
    Lipila Fee Collection System
    Creator: Sangwani P. Zyambo

    module that defines the lipila app views.
"""
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

import os
from lipila_app.db import get_db, current_app
from helpers import (
    generate_pdf, apology, get_payments, get_student, get_receipts,
    get_student_id
    )

from momo.momo import Momo
from momo.mtn_momo import MTN
from momo.airtel_momo import Airtel

bp = Blueprint('lipila', __name__, url_prefix='/lipila')


@bp.route('/home', methods = ['GET', 'POST'])
def index():
    return render_template('payment/index.html')
    
@bp.route('/pay', methods = ['GET', 'POST'])
def pay():
    session.clear()
    error = None

    if request.method == 'POST':
        code = request.form['student']

        if not code:
            error = "Provide student code"
        if not isinstance(code, str):
            error = "Invalid code"
        if len(code) < 7:
            error = "Invalid code"

        student = get_student_id(code)
        if student is not None:
            return redirect(url_for('lipila.get_student_data', id=student))
        else:
            error = "Invalid code"
        flash(error)
    return render_template('payment/pay.html')


@bp.route('payment/<id>', methods = ['GET', 'POST'])
def get_student_data(id):
    conn = get_db()
    db = conn.cursor()
    error = None

    if request.method == 'GET':
        student = get_student(id)

        if error is None:
            db.execute('SELECT school FROM student WHERE id=%s',(id,))
            school_id = db.fetchone()

            db.execute('SELECT school FROM school WHERE id=%s',(school_id[0],))
            school = db.fetchone()

            session['user-id'] = int(id)
            session['firstname'] = student[2]
            session['lastname'] = student[3]
            session['school'] = school[0]
            session['tuition'] = student[7]
            session['student'] = student[2] + ' ' + student[3]
            session['school-id'] = school_id[0]

            return render_template('payment/confirm.html', student=student, school=school)
        flash(error)
    return render_template('payment/pay.html')

    
@bp.route('/confirmed', methods = ['GET', 'POST'])
def confirmed():
    # return "Index"
    if request.method == 'GET':
        data = {
            'id':session['user-id'],
            'fname':session['firstname'],
            'lname':session['lastname'],
            'school':session['school'],
            'tuition':session['tuition']
            }
        return render_template('payment/confirmed.html', data=data)

    amount = request.form['amount']
    account = request.form['mobile']
    if not amount:
        flash('amount missing')
        student = {'firstname':session['firstname'], 'lastname':session['lastname']}
        return render_template('payment/confirm.html', student=student, school=session['school'])
    elif not account:
        flash('account missing')
        student = {'firstname':session['firstname'], 'lastname':session['lastname']}
        return render_template('payment/confirm.html', student=student, school=session['school'])
    else:
        nets = Momo()
        net = nets.get_network(account)
        if net =='mtn':
            session['account'] = account
        elif net =='airtel':
            session['account'] = account
        else:
            session['account'] = 'None'
        session['amount'] = int(amount)
        

    return redirect(url_for('lipila.payment'))

@bp.route('/payment', methods=['GET', 'POST'])
def payment():
    conn = get_db()
    db = conn.cursor()
    partyId = session['account']
    user = session['user-id']
    amount = str(session['amount'])
    externalId = '1234'
    firstname = get_student(user)[2]
    lastname = get_student(user)[3]

    error =  None
        
    if request.method == 'GET':
        net = Momo().get_network(partyId)

        if net == 'mtn' or net == 'airtel':
            session['net'] = net
        else:
            session['net'] = None
            flash('Failed to verify account')
            student = {'firstname':session['firstname'], 'lastname':session['lastname']}
            return render_template('payment/confirm.html', student=student, school=session['school'])
        return render_template('payment/payment.html')
    
    if session['net'] == 'mtn':
        sp = MTN()
        # create momo api sandbox user
        api_user = sp.create_api_user()
        api_key = sp.get_api_key()
        api_token = sp.get_api_token()
        payment = sp.request_to_pay(amount, partyId, externalId)
        if payment == "error":
            return apology('Amount must be greater than 20', 403)
        if payment.status_code == 202:
            try:
                db.execute("INSERT INTO payment (student_id, firstname, lastname, amount, school, account_number) \
                    VALUES(%s,%s,%s,%s,%s,%s)",(user, firstname, lastname, amount, session['school-id'], partyId),
                    )
                conn.commit()
                
                db.execute(
                    "SELECT * FROM student WHERE id=%s",(user,)
                )
                student = db.fetchone()
                
                names =  student[1] + ' ' + student[2]

                msg = 'Success Payment for' + ' ' + names
            
                flash(msg)
            except TypeError as e:
                flash('error')
    
    elif session['net'] == 'airtel':
        sp = Airtel()
        payment = sp.make_payment(partyId, amount)
        if payment:
            try:
                db.execute("INSERT INTO payment (student_id, firstname, lastname, amount, school, account_number) \
                    VALUES(%s,%s,%s,%s,%s,%s)",(user, firstname, lastname, amount, session['school-id'], partyId),
                    )
                db.execute(
                    "SELECT * FROM payment WHERE student_id=%s",(user,)
                    )
                payment = db.fetchone()

                conn.commit()
                db.execute(
                    "SELECT * FROM student WHERE id=%s",(user,)
                )
                student = db.fetchone()

                names =  student[1] + ' ' + student[2]

                msg = 'Success! Payment for' + ' ' + names
            
                flash(msg)
            except Exception as e:
                flash('Exception')
    else:
        error = 'error occured'
        flash(error)
    return redirect(url_for('lipila.show_history'))


@bp.route('/history', methods=['GET', 'POST'])
def show_history():
    user = session['user-id']

    payment = get_payments(user)

    return render_template('payment/history.html', school=session['school'], data=payment)


@bp.route('/download/<receipt>', methods=['GET', 'POST'])
def download(receipt):
    """ downloads a pdf receipt"""
    path = current_app.root_path
    data = get_receipts(receipt)
    rec = generate_pdf(data)
    file_path = os.path.join(path, rec).replace('\\', '/')
  

    return render_template('payment/download.html', id=receipt, file_path=file_path)