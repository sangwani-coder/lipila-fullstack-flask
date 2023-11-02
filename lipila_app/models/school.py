from lipila_app import db
import datetime

class Administrators(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(64))
    email = db.Column(db.Unicode(64))
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)

    def __unicode__(self):
        return self.name
    

class Schools(db.Model):
    """
        Representation of a school
    """
    __tablename__ = 'schools'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(155), nullable=False, unique=True)
    address = db.Column(db.String(255), nullable=False, unique=False)
    city = db.Column(db.String(55), nullable=False, unique=False)
    short_name = db.Column(db.String(55), nullable=False, unique=True)
    # administrators = db.relationship(Administrators, backref="student", cascade="all, delete-orphan")


class Parents(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(64))
    email = db.Column(db.Unicode(64))
    mobile = db.Column(db.Unicode(64))
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    # wards = db.relationship(Students, backref="student", cascade="all, delete-orphan")


    def __unicode__(self):
        return self.name


class Students(db.Model):
    """
        Representation of a students
    """
    __tablename__ = 'student'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Unicode(64))
    middle_name = db.Column(db.Unicode(64))
    last_name = db.Column(db.Unicode(64))
    active = db.Column(db.Boolean, default=True)
    # parent = db.relationship(Parents, backref="student", cascade="all, delete-orphan")
    # school = db.relationship(Schools, backref="student", cascade="all, delete-orphan")
    # school_fees = db.relationship(SchoolFees, backref="student", cascade="all, delete-orphan")
    # other_fees = db.relationship(OtherlFees, backref="student", cascade="all, delete-orphan")
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)

    def __unicode__(self):
        return self.first_name
    

class SchoolFees(db.Model):
    __tablename__ = "schoolfees"

    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.Unicode(64))
    amount = db.Column(db.Float)
    duedate = db.Column(db.DateTime)
    # school = db.relationship(Schools, backref="student", cascade="all, delete-orphan")


class OtherFees(db.Model):
    __tablename__ = "otherfees"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Unicode(64))
    amount = db.Column(db.Float)
    duedate = db.Column(db.DateTime)
    # school = db.relationship(Schools, backref="student", cascade="all, delete-orphan")


class Payments(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    payment_method = db.Column(db.Unicode(64))
    account_number = db.Column(db.Unicode(64))
    status = db.Column(db.Unicode(64))
    # school = db.relationship(Schools, backref="student", cascade="all, delete-orphan")
    # student = db.relationship(Students, backref="student", cascade="all, delete-orphan")