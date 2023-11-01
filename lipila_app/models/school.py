from lipila_app import db

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