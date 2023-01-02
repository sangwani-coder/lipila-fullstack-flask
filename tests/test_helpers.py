
from lipila.helpers import (
    generate_pdf, send_email,
    get_student, get_user, search_email
    )
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


def test_get_user(app):
    """ test the function that gets an admins data"""
    with app.app_context():
        user = get_user(1)
        assert user[0] == 1
        assert user[2] == 'academy'

def test_search_email(app):
    with app.app_context():
        email = search_email("pz@mail.com")
        assert email is None
        email = search_email("zyambo@icloud.com")
        assert email is not None
