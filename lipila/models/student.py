# from sqlalchemy import Column
# from sqlalchemy import Integer
# from sqlalchemy import String
# from sqlalchemy import ForeignKey
# from sqlalchemy.orm import relationship
# from models.base_model import BaseModel, Base


# class Student(BaseModel, Base):
#     """
#         Representation of a student
#     """
#     __tablename__ = 'student'

#     id = Column(Integer, primary_key=True)
#     firstname = Column(String(50), nullable=False)
#     lastname = Column(String(50), nullable=False)
#     school_id = Column(Integer, ForeignKey("school.id"), nullable=False)
#     program = Column(String(255))
#     tuition = Column(Integer)
