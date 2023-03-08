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
from flask import render_template, session

from lipila.db import current_app, get_db
from datetime import datetime

ALLOWED_EXTENSIONS = {'csv', 'xlsx',}

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
        "SELECT school FROM school WHERE id=%s",(data[9],)
    )
    school = db.fetchone()
    print(school)
    student_payment_data = {
        'id':data[0] ,
        'student_id':data[1] ,
        'firstname':data[2] ,
        'lastname':data[3] ,
        'created':data[4] ,
        'amount':data[5] ,
        'account_number':data[8] ,
        'school':school[0].upper()
    }
    my_canvas = canvas.Canvas(file_path, pagesize=letter)
    my_canvas.setLineWidth(.3)
    my_canvas.setFont('Helvetica', 12)
    my_canvas.drawString(30, 750, 'PAYMENT RECEIPT {}'.format(student_payment_data['student_id']))
    my_canvas.drawString(30, 735, 'SCHOOL: {}'.format(student_payment_data['school']))
    my_canvas.drawString(500, 720, "{}".format(student_payment_data['created']))
    my_canvas.line(480, 747, 580, 747)
    my_canvas.drawString(275, 725, 'AMOUNT PAID:')
    my_canvas.drawString(500, 725, "K{}".format(student_payment_data['amount']))
    my_canvas.line(378, 723, 580, 723)
    my_canvas.drawString(30, 703, 'RECEIVED BY: {}'.format(""))
    my_canvas.line(120, 700, 580, 700)
    my_canvas.drawString(120, 703, "STUDENT ID: {}".format(student_payment_data['student_id']))
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
    total_paid = 0
    size = 0 

    if period == "all":
        db.execute(
            "SELECT amount FROM payment WHERE school=%s",(id,)
        )
        pays = db.fetchall()
        # pays = [()]
        size = len(pays)
        for i in range(size):
            total_paid = total_paid + pays[i][0]

    elif period == "month":
        month = datetime.now().strftime("%m")
        year = datetime.now().strftime("%Y")
        db.execute(
            "SELECT * FROM payment WHERE school=%s AND\
                  extract(year from created)=%s AND \
                    extract(month from created)=%s",(id, year, month)
        )
        data_month = db.fetchall()
        size = len(data_month)
        for i in range(size):
            total_paid = total_paid + data_month[i][5]

    elif period == "week":
        year = datetime.now().strftime("%Y")
        week = datetime.now().strftime("%U")
        db.execute(
            "SELECT * FROM payment WHERE school=%s AND\
                  extract(year from created)=%s AND \
                    extract(week from created)=%s",(id, year, week)
        )
        data_week = db.fetchall()
        size = len(data_week)
        for i in range(size):
            total_paid = total_paid + data_week[i][5]

    elif period == "day":
        year = datetime.now().strftime("%Y")
        month = datetime.now().strftime("%m")
        day = datetime.now().strftime("%d")
        
        db.execute(
            "SELECT * FROM payment WHERE school=%s AND\
                  extract(year from created)=%s AND \
                  extract(month from created)=%s AND \
                    extract(day from created)=%s",(id, year, month, day)
        )
        data_day = db.fetchall()
        size = len(data_day)
        for i in range(size):
            total_paid = total_paid + data_day[i][5]

    return [total_paid, size]


def show_recent(user_id, filter):
    """
        Selects all recent payments for the user/school id.
        Select payments within the current month
        params:
            id: the school id.
    """
    conn = get_db()
    db = conn.cursor()

    # find the schools id
    db.execute(
            "SELECT * from school WHERE id=%s",(user_id,)
        )
    data = db.fetchone()
    school_id = str(data[0])

    # filter
    if filter == "all":
        db.execute(
            "SELECT * FROM payment WHERE school=%s",(school_id,)
        )
               
    elif filter == "month":
        month = datetime.now().strftime("%m")
        year = datetime.now().strftime("%Y")
        db.execute(
            "SELECT * FROM payment WHERE school=%s AND\
                  extract(year from created)=%s AND \
                    extract(month from created)=%s",(school_id, year, month)
        )
        

    elif filter == "week":
        year = datetime.now().strftime("%Y")
        week = datetime.now().strftime("%U")
        db.execute(
            "SELECT * FROM payment WHERE school=%s AND\
                  extract(year from created)=%s AND \
                    extract(week from created)=%s",(school_id, year, week)
        )
        

    elif filter == "today":
        year = datetime.now().strftime("%Y")
        month = datetime.now().strftime("%m")
        day = datetime.now().strftime("%d")
        
        db.execute(
            "SELECT * FROM payment WHERE school=%s AND\
                  extract(year from created)=%s AND \
                  extract(month from created)=%s AND \
                    extract(day from created)=%s",(school_id, year, month, day)
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
    if code is not None:
        return code[0]
    return None

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

def upload_excel_file(file):
    """
        Function to upload and read spreadsheet or csv data
    """

    import csv
    import pandas

    f = file.split(".")[1]
    if f == "xlsx":
        with open(file, 'rb') as f:
            excel_data_df = pandas.read_excel(f, sheet_name='students')
            # print whole sheet data
        return excel_data_df.to_dict(orient='record')

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

def add_uploaded_data(data):
    conn = get_db()
    db = conn.cursor()
    error = None
    for student in range(len(data)):
        firstname = data[student]['firstname']
        lastname = data[student]['lastname']
        school = session['user_id']
        tuition = data[student]['tuition']
        program = data[student]['program']

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
                msg = 'students added successfully.'
                
        # msg = error
    return msg