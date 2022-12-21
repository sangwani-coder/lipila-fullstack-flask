from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from skoolpay.db import get_db

from skoolpay.momo.momo import Momo
from skoolpay.momo import mtn_momo, airtel_momo 

bp = Blueprint('skoolpay', __name__, url_prefix='/skoolpay')


# a simple page that says hello
@bp.route('/', methods = ['GET', 'POST'])
def homepage():
    # return "Index"
    if request.method == 'POST':
        student = request.form['student']
        print(student)
        return redirect(url_for('skoolpay.get_student_data', id=student))
    return render_template('payment/index.html')


@bp.route('payment/<id>', methods = ['GET', 'POST'])
def get_student_data(id):
    db = get_db()
    error = None

    if request.method == 'GET':
        student =  db.execute('SELECT * FROM student WHERE id=?',(id,)).fetchone()

        if student is None:
            error = 'No student found!'
        if error is None:
            school_id = db.execute('SELECT school FROM student WHERE id=?',(id,)).fetchone()
            school = db.execute('SELECT school FROM school WHERE id=?',(school_id['school'],)).fetchone()

            session['user-id'] = int(id)
            session['firstname'] = student['firstname']
            session['lastname'] = student['lastname']
            session['school'] = school['school']
            session['tuition'] = student['tuition']

            return render_template('payment/confirm.html', student=student, school=school['school'])
    flash(error)
    return render_template('payment/index.html')

    
@bp.route('/confirmed', methods = ['GET', 'POST'])
def confirmed():
    # return "Index"
    if request.method == 'GET':
        data = {
            # 'amount':session['amount'],
            # 'account':session['account'],
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
    elif not account:
        flash('account missing')
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
        

    return redirect(url_for('skoolpay.payment'))

@bp.route('/payment', methods=['GET', 'POST'])
def payment():

    acct = session['account']
    user = session['user-id']
    amount = session['amount']
        
    if request.method == 'GET':
        net = Momo().get_network(acct)

        if net == 'mtn' or net == 'airtel':
            session['net'] = net
        else:
            session['net'] = None
            flash('Failed to verify account')
        return render_template('/payment/payment.html')
    
    if session['net'] == 'mtn':
        sp = mtn_momo.MTN()
        payment = sp.make_payment(acct, amount)
        if payment == 'Success':
            db = get_db()
        
            db.execute("INSERT INTO payment (student_id, amount, account_number) \
                VALUES(?,?,?)",(user, amount, acct),
                )
    
    elif session['net'] == 'airtel':
        sp = airtel_momo.Airtel()
        payment = sp.make_payment(acct, amount)
        if payment == 'Success':
            db = get_db()
        
            db.execute("INSERT INTO payment (student_id, amount, account_number) \
                VALUES(?,?,?)",(user, amount, acct),
                )

    flash('success')
    return render_template('/payment/index.html')

