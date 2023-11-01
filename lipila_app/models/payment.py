# from lipila_app import db

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
    
  