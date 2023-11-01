import datetime

from lipila_app import db
from .school import Schools

class Students(db.Model):
    """
        Representation of a students
    """
    __tablename__ = 'student'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Unicode(64))
    middle_name = db.Column(db.Unicode(64))
    last_name = db.Column(db.Unicode(64))
    email = db.Column(db.Unicode(64))
    active = db.Column(db.Boolean, default=True)
    # school = db.relationship(Schools, backref="student", cascade="all, delete-orphan")
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)

    def __unicode__(self):
        return self.first_name