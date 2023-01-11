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
from lipila.db import get_db
from lipila.db import current_app
from lipila.helpers import (
    generate_pdf, apology, get_payments, get_student, get_receipts,
    get_students_school
    )

from lipila.momo.momo import Momo
from lipila.momo.mtn_momo import MTN
from lipila.momo.airtel_momo import Airtel

bp = Blueprint('lipila', __name__, url_prefix='/lipila')


@bp.route('/home', methods = ['GET', 'POST'])
def index():
    """ Homepage for the student"""
    return render_template('payment/index.html')
    
@bp.route('/pay', methods = ['GET', 'POST'])
def pay():
    """ View that renders a template for a student to`
        enter their payment code and redirects to the
        set_student_session view.
    """
    session.clear()
    if request.method == 'POST':
        student = request.form['student']
        session['std'] = int(student)
        return redirect(url_for('lipila.selection', id=int(student)))
    return render_template('payment/pay.html')

@bp.route('/selection', methods = ['GET', 'POST'])
def selection():
    """ view that returns a template for a user to
        choose what items they want to pay for.
    """
    if request.method == 'POST':
        tuition = request.form.get('tuition')
        transport = request.form.get('transport')
        extra = request.form.get('extra')
        uniform = request.form.get('uniform')
        error = None

        if not tuition and not transport and not extra and not uniform:
            error = "You must select at least one option"
            flash(error)
            return render_template('payment/options.html')

        items = {}
        if tuition:
            session['tuition'] = tuition
            items['tuition'] = tuition
        if transport:
            session['transport'] = transport
            items['transport'] = transport
        if extra:
            session['extra'] = extra
            items['extra'] = extra
        if uniform:
            session['uniform'] = uniform
            items['uniform'] = uniform

        session['items'] = items

        return redirect(url_for('lipila.set_student_session', id=session['std']))
    return render_template('payment/options.html')


@bp.route('payment/<id>', methods = ['GET', 'POST'])
def set_student_session(id):
    """ View function that gets a students data from the database
        and sets a students session informaiton.
    """
    error = None

    if request.method == 'GET':
        student = get_student(id)

        if student is None:
            error = 'No student found!'
        if error is None:
            items = session['items']
            session['user-id'] = id
            school = get_students_school(id)
            session['firstname'] = student[1]
            session['lastname'] = student[2]
            session['school'] = school[1][0]
            session['tuition'] = student[6]
            session['student'] = student[1] + ' ' + student[2]
            session['school-id'] = school[0][0]

            return render_template('payment/confirm.html',
                                    student=student, school=school, items=items)
    flash(error)
    return render_template('payment/index.html')


@bp.route('/confirmed', methods = ['GET', 'POST'])
def confirmed():
    """ view function displays payment details for student
        to final confirmation and gets the amount and account number
        from the submitted form.
    """
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
        student = {
                    'firstname':session['firstname'],
                    'lastname':session['lastname']}
        return render_template('payment/confirm.html',
                                student=student, school=session['school'])
    elif not account:
        flash('account missing')
        student = {
                    'firstname':session['firstname'],
                    'lastname':session['lastname']}
        return render_template('payment/confirm.html', 
                                student=student, school=session['school'])
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
    """ view function that queries that queries the momo APIs"""
    conn = get_db()
    db = conn.cursor()
    partyId = session['account']
    user = session['user-id']
    amount = str(session['amount'])
    externalId = '1234'
    firstname = get_student(user)[1]
    lastname = get_student(user)[2]

    error =  None
        
    if request.method == 'GET':
        net = Momo().get_network(partyId)

        if net == 'mtn' or net == 'airtel':
            session['net'] = net
        else:
            session['net'] = None
            flash('Failed to verify account')
            student = {
                        'firstname':session['firstname'],
                        'lastname':session['lastname']}
            return render_template('payment/confirm.html',
                                    student=student, school=session['school'])
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
            # If the request to the mtn api was successful insert 
            # the payment in the database.
            try:
                db.execute("INSERT INTO payment (student_id, firstname,\
                    lastname, amount, school, account_number) \
                    VALUES(%s,%s,%s,%s,%s,%s)",(user, firstname, lastname,
                    amount, session['school-id'], partyId),
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
                db.execute("INSERT INTO payment (student_id, firstname,\
                    lastname, amount, school, account_number) \
                    VALUES(%s,%s,%s,%s,%s,%s)",(user, firstname, lastname,
                    amount, session['school-id'], partyId),
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
    """ view that returns a page showing a students previous transactions"""
    user = session['user-id']

    payment = get_payments(user)

    return render_template('payment/history.html', 
                            school=session['school'], data=payment)


@bp.route('/download/<receipt>', methods=['GET', 'POST'])
def download(receipt):
    """ downloads a pdf receipt"""
    path = current_app.root_path
    data = get_receipts(receipt)
    rec = generate_pdf(data)
    file_path = os.path.join(path, rec).replace('\\', '/')
  

    return render_template('payment/download.html',
                            id=receipt, file_path=file_path)