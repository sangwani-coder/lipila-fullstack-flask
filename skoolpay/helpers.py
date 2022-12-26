""" Create and generate pdf invoice"""

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

from skoolpay.db import current_app

def generate_pdf(data):
    """helper function to generate"""
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