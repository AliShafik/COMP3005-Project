from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

# Define Table Classes
Base = declarative_base()

class Member(Base):
    #Schema
    __tablename__ = "Member"
    member_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=True)
    gender = Column(String, nullable=True)
    contact_detail = Column(String, nullable=False)

    #Print statment
    def __repr__(self):
        return f"({self.member_id}, {self.name}, {self.date_of_birth}, {self.gender}, {self.contact_detail})"
    
