""" 
    helpers.py
    Lipila Fee Collection System
    Creator: Sangwani P. Zyambo

    Module that defines helper functions for the views.

    Functions:
        generate_pdf: Function that generates a pdf invoice.
        apology: Function that renders the apology page.
        calculate_mount: Function that calculates the total payments received.
        show_recent: Funciton that returns recent payments to the admin dashboard page
        get_student: Function that selects a single student matching id from the database.
        get_students: Function to selects all students from the database matching the user id.
        get_user" Function that selects a user from the school table matching id.
        send_email: Function that sends an email to the provided email parameter.
        search_email: Function that searches if a submited email  exisrs in the database.
        get_payments: Function that gets all payments from the database that match a student id.
        format_date: Function to forma the date.
"""

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
from flask import render_template

from lipila.db import current_app, get_db

ALLOWED_EXTENSIONS = {'csv'}

def generate_pdf(data):
    """
       Function that generates a pdf format of the invoice.
       param:
        data: The data to put in the invoice.
    """
    directory = os.path.join(current_app.root_path, 'receipts').replace('\\','/')
    filename = "receipt-{}.pdf".format(data[0])
    file_path = os.path.join(directory, filename).replace('\\', '/')

    if not os.path.isdir(directory):
        os.mkdir(directory)

    conn = get_db()
    db = conn.cursor()

    db.execute(
        "SELECT school FROM school WHERE id=%s",(data[7],)
    )
    school = db.fetchone()

    p_data = {
        'id':data[0] ,
        'student_id':data[1] ,
        'firstname':data[2] ,
        'lastname':data[3] ,
        'created':data[4] ,
        'amount':data[5] ,
        'account_number':data[6] ,
        'school':school[0].upper()
    }
    my_canvas = canvas.Canvas(file_path, pagesize=letter)
    my_canvas.setLineWidth(.3)
    my_canvas.setFont('Helvetica', 12)
    my_canvas.drawString(30, 750, 'PAYMENT RECEIPT {}'.format(p_data['student_id']))
    my_canvas.drawString(30, 735, 'SCHOOL: {}'.format(p_data['school']))
    my_canvas.drawString(500, 720, "{}".format(p_data['created']))
    my_canvas.line(480, 747, 580, 747)
    my_canvas.drawString(275, 725, 'AMOUNT PAID:')
    my_canvas.drawString(500, 725, "K{}".format(p_data['amount']))
    my_canvas.line(378, 723, 580, 723)
    my_canvas.drawString(30, 703, 'RECEIVED BY: {}'.format(""))
    my_canvas.line(120, 700, 580, 700)
    my_canvas.drawString(120, 703, "STUDENT ID: {}".format(p_data['student_id']))
    my_canvas.save()

    return file_path

def apology(message, code=400):
    """
        Render message as an apology to user.
        params:
            message: The message to render to user.
            code: the error code to show on page.
    """
    def escape(s):
        """
        Escape special characters.
        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def calculate_amount(period, id):
    """ 
        Calculates the total payments made for each period.
        params:
            period: the day, week or month to make calculations for.
            id: The user id.
    """
    conn = get_db()
    db = conn.cursor()
    total = 0

    if period == "all":
        db.execute(
            "SELECT amount FROM payment WHERE school=%s",(id,)
        )
        pays = db.fetchall()
        # pays = [()]
        size = len(pays)
        for i in range(size):
            total = total + pays[i][0]

    elif period == "month":
        db.execute(
        "SELECT * FROM payment WHERE school=%s AND created=date('now')",(id,)
    )
        data_month = db.fetchall()
        size = len(data_month)
        for i in range(size):
            total = total + data_month[i][0]

    elif period == "week":
        db.execute(
        "SELECT * FROM payment WHERE school=%s AND created=date('now')",(id,)
    )
        data_week = db.fetchall()
        size = len(data_week)
        for i in range(size):
            total = total + data_week[i][0]

    elif period == "day":
        db.execute(
            "SELECT * FROM payment WHERE school=%s AND created=date('now')",(id,)
    )
        data_day = db.fetchall()
        size = len(data_day)
        for i in range(size):
            total = total + data_day[i][0]

    return total

def calculate_payments(period, id):
    """ 
        calculates the total amount paid for each given period.
        params:
            period: the day, week or month to calculate payments.
            id: the user id.
    """
    conn = get_db()
    db = conn.cursor()

    if period == "all":
        db.execute(
            "SELECT * FROM payment WHERE school=%s",(id,)
        )
        pays = db.fetchall()
        return len(pays)

    if period == "month":
        db.execute(
            "SELECT * FROM payment WHERE school=%s AND created=date('now')",(id,)
        )
        pays = db.fetchall()
        return len(pays)

    elif period == "week":
        db.execute(
            "SELECT * FROM payment WHERE school=%s AND created=date('now')",(id,)
        )
        pays = db.fetchall()
        return len(pays)

    elif period == "day":
        db.execute(
            "SELECT * FROM payment WHERE school=%s AND created=date('now')",(id,)
        )
        pays = db.fetchall()
        return len(pays)

def show_recent(id):
    """
        Selects all recent payments for the user/school id.
        params:
            id: the school id.
    """
    conn = get_db()
    db = conn.cursor()

    db.execute(
            "SELECT * from school WHERE id=%s",(id,)
        )
    school = db.fetchone()

    id = str(school[0])
    db.execute(
            "SELECT * FROM payment WHERE school=%s",(id,)
        )
    payment = db.fetchall()

    return payment

def get_student(id):
    """
        get a students information from the student table.
        parmas:
            id: the student id.
    """
    conn = get_db()
    db = conn.cursor()

    db.execute(
        "SELECT * FROM student WHERE id=%s", (id,)
    )
    data = db.fetchone()

    if data is None:
        apology("Student not found", 404)

    return data

def get_student_id(code):
    """
        get a students id
    """
    conn = get_db()
    db = conn.cursor()

    db.execute(
        "SELECT id FROM student WHERE payment_code=%s", (code,)
    )
    code = db.fetchone()

    return code[0]

def get_number_of_students():
    """
        get the whole number of students in the database.
    """
    conn = get_db()
    db = conn.cursor()

    db.execute(
        "SELECT * FROM student"
    )
    data = db.fetchall()

    size = len(data)

    return size + 1

def get_students(id):
    """
        get all students information from the student table
        param:
            id: the school id
    """
    pass

def get_user(id):
    """
        get an admin users information from the school table.
        params:
            id: the school id.
    """
    conn = get_db()
    db = conn.cursor()

    db.execute(
        "SELECT * FROM school WHERE id=%s", (id,)
    )
    data = db.fetchone()

    if data is None:
        apology("User not found", 404)

    return data

def send_email(email:str, subject:str, body:str, message:str)-> str:
    """ 
        Sends an email to a user.
        params:
            email: the recievers email.
            subject: the email subject.
            body: the main message.
            message: the message to flask to the user.
    """
    from flask import current_app
    from flask_mail import Mail, Message

    app = current_app
    mail = Mail(app)
    msg = Message(
        subject,
        sender ='lipila.info@gmail.com',
        recipients = [email]
        )
    msg.body = body
    mail.send(msg)
    return message

def search_email(email):
    """
        search for user email.
        params:
            email: The email to look up in the school table.
    """
    conn = get_db()
    db = conn.cursor()

    db.execute(
        "SELECT * FROM school WHERE email=%s",(email,)
    )
    user = db.fetchone()
    return user

def get_payments(id):
    """
        get all payments matching student id.
    """
    conn = get_db()
    db = conn.cursor()
    db.execute(
        "SELECT * FROM payment WHERE student_id =%s",(id,)
    )
    payments = db.fetchall()
    return payments


def get_receipts(id):
    """
        get single payments matching student id.
    """
    conn = get_db()
    db = conn.cursor()
    db.execute(
        "SELECT * FROM payment WHERE id =%s",(id,)
    )
    payments = db.fetchone()
    return payments

def format_date(date):
    """
        string format a date object to readable format
    """
    f_date = date.strftime("%b %d %Y %H:%M:%S")

    return f_date

def upload(file):
    """ reads and writes student data"""

    import csv
    with open('file.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            print(row)

def allowed_file(filename):
    """Checks if the uploaded file extension is suppoerted
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_pay_code(firstname: str, lastname:str, id: str)-> str:
    """function that generates a students payment code"""
    f_initial = firstname[0].upper()
    l_initial = lastname[0].upper()
    base = f_initial + l_initial + '23'
    
    pay_code = ''

    if int(id) < 10:
        pay_code =  base + '000' + str(id)

    elif int(id) >= 10 or int(id) < 99:
        pay_code =  base + '00' + str(id)

    elif int(id) >= 100 or int(id) < 999:
        pay_code = base + '0' + str(id)

    elif int(id) >= 1000:
        pay_code = base + str(id)
   
    return pay_code