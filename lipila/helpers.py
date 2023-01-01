""" HELPER METHODS"""

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
from flask import render_template

from lipila.db import current_app, get_db

def generate_pdf(data):
    """helper function to generate pdf"""
    directory = os.path.join(current_app.root_path, 'receipts').replace('\\','/')
    filename = "receipt-{}.pdf".format(data[0])
    file_path = os.path.join(directory, filename).replace('\\', '/')

    if not os.path.isdir(directory):
        os.mkdir(directory)

    my_canvas = canvas.Canvas(file_path, pagesize=letter)
    my_canvas.setLineWidth(.3)
    my_canvas.setFont('Helvetica', 12)
    my_canvas.drawString(30, 750, 'PAYMENT RECEIPT {}'.format(data[0]))
    my_canvas.drawString(30, 735, 'SCHOOL: {}'.format(data[5]))
    my_canvas.drawString(500, 720, "{}".format(data[2]))
    my_canvas.line(480, 747, 580, 747)
    my_canvas.drawString(275, 725, 'AMOUNT OWED:')
    my_canvas.drawString(500, 725, "${}".format(data[3]))
    my_canvas.line(378, 723, 580, 723)
    my_canvas.drawString(30, 703, 'RECEIVED BY:')
    my_canvas.line(120, 700, 580, 700)
    my_canvas.drawString(120, 703, "STUDENT ID: {}".format(data[1]))
    my_canvas.save()

    return file_path

def apology(message, code=400):
    """Render message as an apology to user."""
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
        Calculates the total payments made for each period
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
        calculates the total amount paid for each given period
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
    """ Show recent payments"""
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
    """ get a students information"""
    conn = get_db()
    db = conn.cursor()

    db.execute(
        "SELECT * FROM student WHERE id=%s", (id,)
    )
    data = db.fetchone()

    if data is None:
        apology("Student not found", 404)

    return data

def get_students(id):
    """ get all students information"""
    pass

def send_email(email:str, subject:str, body:str, ms:str)-> str:
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
    return ms