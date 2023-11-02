from lipila_app import db
import datetime
from sqlalchemy_utils import EmailType, UUIDType, URLType, CurrencyType
import uuid


class Administrator(db.Model):
    id = db.Column(UUIDType(binary=False), default=uuid.uuid4, primary_key=True)
    name = db.Column(db.Unicode(64))
    email = db.Column(EmailType, unique=True, nullable=False)
    website = db.Column(URLType)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    # related school
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))
    school = db.relationship('School', foreign_keys=[school_id])

    def __unicode__(self):
        return self.name
    

class School(db.Model):
    """
        Representation of a school
    """
    __tablename__ = 'school'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(155), nullable=False, unique=True)
    address = db.Column(db.String(255), nullable=False, unique=False)
    city = db.Column(db.String(55), nullable=False, unique=False)
    short_name = db.Column(db.String(55), nullable=True, unique=True)

    admin_id = db.Column(UUIDType(binary=False), db.ForeignKey(Administrator.id))
    admin = db.relationship(Administrator, foreign_keys=[admin_id], backref='zyambo')


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
    # school = db.relationship(School, backref="student", cascade="all, delete-orphan")
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
    # school = db.relationship(School, backref="student", cascade="all, delete-orphan")
    


class OtherFees(db.Model):
    __tablename__ = "otherfees"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Unicode(64))
    amount = db.Column(db.Float)
    duedate = db.Column(db.DateTime)
    # school = db.relationship(School, backref="student", cascade="all, delete-orphan")


class Payments(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    payment_method = db.Column(db.Unicode(64))
    account_number = db.Column(db.Unicode(64))
    status = db.Column(db.Unicode(64))
    # school = db.relationship(School, backref="student", cascade="all, delete-orphan")
    # student = db.relationship(Students, backref="student", cascade="all, delete-orphan")