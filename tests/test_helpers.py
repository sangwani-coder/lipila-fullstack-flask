
from lipila.helpers import generate_pdf, send_email, get_student
from lipila.db import get_db

def test_send_mail(app):
    """ test the function to send emails"""
    email = "mightypz@gmail.com"
    subject = "registration"
    body = "Hello from Lipila application"
    ms = "Email Sent Succesfully"

    with app.app_context():
        msg = send_email(email, subject, body, ms)
        assert msg == ms


def test_get_student(app):
    """ test the function that gets a students data"""
    with app.app_context():
        student = get_student(2)
        assert student[0] == 2
        assert student[1] == 'pita'
        assert student[2] == 'zed'
        assert student[4] == 'IT'
        assert student[5] == 300