"""
    helpers_2
    second module with helper functions
"""
from datetime import datetime
from lipila.db import get_db


def calculate_any_pending_balance(id:int, amount: int, term: str)-> int:
    """check the balance"""
    year = int(datetime.now().strftime("%Y"))

    balance = 0
    previous_term_payment = 0

    conn = get_db()
    db = conn.cursor()
    db.execute(
        "SELECT tuition FROM student WHERE student_id =%s",(id,)
        )
    tuition = db.fetchone()
    students_tuition_per_term = tuition[0]

    if term == "one":
        # check previous year term3
        term = "three"
        year = year - 1
        db.execute(
            "SELECT amount FROM payment WHERE student_id =%s \
                AND extract (year from created)=%s AND term=%s",(id, year, term)
                )
        paid = db.fetchone()
        if paid is not None:
            previous_term_payment = paid[0]

    elif term == "two":
        #check term one
        term = "one"
        db.execute(
           "SELECT amount FROM payment WHERE student_id =%s \
                AND extract (year from created)=%s AND term=%s",(id, year, term)
        )
        paid = db.fetchone()
        if paid is not None:
            previous_term_payment = paid[0]


    elif term == "three":
        # check term two
        term = "two"
        db.execute(
            "SELECT amount FROM payment WHERE student_id =%s \
                AND extract (year from created)=%s AND term=%s",(id, year, term)
                )
        paid = db.fetchone()
        if paid is not None:
            previous_term_payment = paid[0]


    balance = previous_term_payment - students_tuition_per_term

    if balance < 0:
        available_cash = amount - balance #pay for selected term
        pend_payment = balance * -1 # pay to previous term
    else:
        available_cash = balance + amount
    return available_cash
    