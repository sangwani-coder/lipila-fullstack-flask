""" HELPER METHODS"""

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
from flask import render_template

from lipila.db import current_app, get_db

def generate_pdf(data):
    """helper function to generate pdf"""
    directory = os.path.join(current_app.root_path, 'receipts').replace('\\','/')
    filename = "receipt-{}.pdf".format(data['id'])
    file_path = os.path.join(directory, filename).replace('\\', '/')

    if not os.path.isdir(directory):
        os.mkdir(directory)

    my_canvas = canvas.Canvas(file_path, pagesize=letter)
    my_canvas.setLineWidth(.3)
    my_canvas.setFont('Helvetica', 12)
    my_canvas.drawString(30, 750, 'PAYMENT RECEIPT {}'.format(data['id']))
    my_canvas.drawString(30, 735, 'SCHOOL: {}'.format(data['school']))
    my_canvas.drawString(500, 720, "{}".format(data['created']))
    my_canvas.line(480, 747, 580, 747)
    my_canvas.drawString(275, 725, 'AMOUNT OWED:')
    my_canvas.drawString(500, 725, "${}".format(data['amount']))
    my_canvas.line(378, 723, 580, 723)
    my_canvas.drawString(30, 703, 'RECEIVED BY:')
    my_canvas.line(120, 700, 580, 700)
    my_canvas.drawString(120, 703, "STUDENT ID: {}".format(data['student_id']))
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
    db = get_db()
    total = 0

    if period == "all":
        pays = db.execute(
            "SELECT amount FROM payment WHERE school=?",(id,)
        ).fetchall()
        size = len(pays)
        for i in range(size):
            total = total + pays[i]['amount']

    elif period == "month":
        data_month = db.execute(
        "SELECT * FROM payment WHERE school=? AND created=date('now')",(id,)
    ).fetchall()
        size = len(data_month)
        for i in range(size):
            total = total + data_month[i]['amount']

    elif period == "week":
         data_week = db.execute(
        "SELECT * FROM payment WHERE school=? AND created=date('now')",(id,)
    ).fetchall()
         size = len(data_week)
         for i in range(size):
            total = total + data_week[i]['amount']

    elif period == "day":
        data_day = db.execute(
            "SELECT * FROM payment WHERE school=? AND created=date('now')",(id,)
    ).fetchall()
        size = len(data_day)
        for i in range(size):
            total = total + data_day[i]['amount']

    return total

def calculate_payments(period, id):
    """ 
        calculates the total amount paid for each given period
    """
    db = get_db()

    if period == "all":
        pays = db.execute(
            "SELECT * FROM payment WHERE school=?",(id,)
        ).fetchall()
        return len(pays)

    if period == "month":
        pays = db.execute(
            "SELECT * FROM payment WHERE school=? AND created=date('now')",(id,)
        ).fetchall()
        return len(pays)

    elif period == "week":
        pays = db.execute(
            "SELECT * FROM payment WHERE school=? AND created=date('now')",(id,)
        ).fetchall()
        return len(pays)

    elif period == "day":
        pays = db.execute(
            "SELECT * FROM payment WHERE school=? AND created=date('now')",(id,)
        ).fetchall()
        return len(pays)

def show_recent(id):
    """ Show recent payments"""
    db = get_db()
    school = db.execute(
            "SELECT * from school WHERE id=?",(id,)
        ).fetchone()

    id = str(school['id'])
    payment = db.execute(
            "SELECT * FROM payment WHERE school=?",(id,)
        ).fetchall()

    return payment