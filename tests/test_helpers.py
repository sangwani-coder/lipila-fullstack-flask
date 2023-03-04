"""
    test_helpers.py
    Lipila Fee Collection System
    Creator: Sangwani P. Zyambo

    unittests for the helper functions.
"""
from lipila.helpers import (
    send_email,
    get_student, get_user, search_email,
    get_payments, format_date, get_receipts,
    allowed_file, generate_pay_code, get_number_of_students,
    get_student_id
    )
from datetime import datetime

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
        assert student[2] == 'pita'
        assert student[3] == 'zed'
        assert student[6] == 'IT'
        assert student[7] == 300

def test_get_user(app):
    """ test the function that gets an admins data"""
    with app.app_context():
        user = get_user(1)
        assert user[0] == 1
        assert isinstance(user[2], datetime)
        assert user[3] == 'academy'

def test_search_email(app):
    with app.app_context():
        email = search_email("pz@mail.com")
        assert email is None
        email = search_email("admin@email.com")
        assert email is not None

def test_get_payments(app):
    with app.app_context():
        payment  = get_payments(1)
        assert payment[0][5] == 500
        assert payment[2][5] == 600
        assert len(payment) == 3
        assert isinstance(payment, list)

def test_get_student_id(app):
    with app.app_context():
        code = get_student_id('JM23013')
        code2= get_student_id('SM23008')
        assert code == 13
        assert code2 == 8

def test_format_date():
    """ test the format_date functions"""
    from datetime import datetime
    date = datetime(2023, 8, 13, 12, 45, 35)
    f_date = format_date(date)

    assert f_date == "Aug 13 2023 12:45:35"

def test_get_receipts(app):
    with app.app_context():
        payment  = get_receipts(1)
        assert payment[2] == 'sepi'
        assert payment[3] == 'zed'
        assert payment[5] == 500
        assert payment[6] == '0971892260'

        payment  = get_receipts(10)
        assert payment[2] == 'sangwa'
        assert payment[3] == 'zed'
        assert payment[5] == 300
        assert payment[6] == '0966698594'

def test_allowed_files():
    """Tests the allowed_files function"""
    file = "test.csv"
    res = allowed_file(file)
    assert res == True
    file = "test.pdf"
    res = allowed_file(file)
    assert res == False

def test_generate_pay_code(app):
    """ Test the helper function that generates a student code"""
    with app.app_context():
        # test student number 2
        student1 = get_student(2)
        id = student1[0] # 2
        fname = student1[2] # pita
        lname = student1[3] # zed

        pay_code = generate_pay_code(fname, lname, id)
        assert pay_code == 'PZ230002'

        # test student number 10
        student2 = get_student(10)
        id2 = student2[0] # 10
        fname2 = student2[2] # nalishebo
        lname2 = student2[3] # zed

        pay_code = generate_pay_code(fname2, lname2, id2)
        assert pay_code == 'NZ230010'

        # test student number 10
        student2 = get_student(14)
        id2 = student2[0] # 10
        fname2 = student2[2] # sangwa
        lname2 = student2[3] # zed

        pay_code = generate_pay_code(fname2, lname2, id2)
        assert pay_code == 'SZ230014'

def test_get_number_of_students(client, auth, app):
    """test the function that counts number of students"""
    with app.app_context():
        available_id = get_number_of_students()
        assert available_id == 15

    response = auth.login()
    assert response.headers['Location'] == '/lipila/admin/dashboard'
    with client:
        assert client.get('/lipila/admin/add').status_code == 200

    response = client.post(
        '/lipila/admin/add', data={
            'firstname':'natasha', 'lastname':'zyambo', 'school':1,
            'program':'b', 'tuition':300,
            }
    )
    response = client.post(
        '/lipila/admin/add', data={
            'firstname':'natasha', 'lastname':'zyambo', 'school':1,
            'program':'b', 'tuition':300,
            }
    )
    with app.app_context():
        available_id = get_number_of_students()
        assert available_id == 17
