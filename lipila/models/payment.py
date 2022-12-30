# from sqlalchemy import Column
# from sqlalchemy import Integer
# from sqlalchemy import String
# from sqlalchemy import ForeignKey
# from sqlalchemy.orm import relationship
# from models.base_model import BaseModel, Base


# class Payment(BaseModel, Base):
#     """
#         Representation of a payment
#     """
#     __tablename__ = 'payment'

#     id = Column(Integer, primary_key=True)
#     student_id = Column(Integer, ForeignKey("student.id"), nullable=False)
#     school_id = Column(String, ForeignKey("school.id"), nullable=False)
#     amount = Column(Integer, nullable=False)
#     account_number = Column(String(50), nullable=False)
    
  