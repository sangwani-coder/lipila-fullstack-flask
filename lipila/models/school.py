from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class School(db.Model):
    """
        Representation of a school
    """
    __tablename__ = 'school'

    id = db.Column(db.Integer, primary_key=True)
    job = db.Column(db.String, nullable=False)
    school = db.relationship("Student", backref="school", cascade="all, delete-orphan")
    email = db.Column(db.String, nullable=False, unique=True)
    mobile = db.Column(db.String, nullable=False)
    reg_number = db.Column(db.String)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)
