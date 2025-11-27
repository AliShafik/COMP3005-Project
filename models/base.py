from sqlalchemy import Column, Integer, String, Date, ForeignKey, Numeric
from sqlalchemy.ext.declarative import declarative_base

# Define Table Classes
Base = declarative_base()

#Schemas

#Member Table
class Member(Base):
    __tablename__ = "Member"
    member_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    date_of_birth = Column(Date, nullable=True)
    gender = Column(String(10), nullable=True)
    contact_detail = Column(String(255), nullable=False)

    #Print statment
    def __repr__(self):
        return f"({self.member_id}, {self.name}, {self.date_of_birth}, {self.gender}, {self.contact_detail})"
    
#Health Metric Table
class HealthMetric(Base):
    __tablename__ = "HealthMetric"
    metric_id = Column(Integer, primary_key=True)
    member_id = Column(Integer, ForeignKey('Member.member_id'), nullable=False)
    date_recorded = Column(Date, nullable=False)
    weight = Column(Numeric(5,2), nullable=True)
    height = Column(Numeric(5,2), nullable=True)
    heart_rate = Column(Integer, nullable=True)
    date_recorded = Column(Date, nullable=True)

    #Print statment
    def __repr__(self):
        return f"({self.metric_id}, {self.member_id}, {self.date_recorded}, {self.weight}, {self.height}, {self.heart_rate}, {self.date_recorded})"

#Billing and Payments Table
class BillingPayment(Base):
    __tablename__ = "BillingPayment"
    billing_id = Column(Integer, primary_key=True)
    member_id = Column(Integer, ForeignKey('Member.member_id'), nullable=False)
    type_of_billing = Column(String(50), nullable=False)
    amount_due = Column(Numeric(10, 2), nullable=False)
    status = Column(String(20), nullable=False)
    payment_method = Column(String(50), nullable=True)

    #Print statment
    def __repr__(self):
        return f"({self.billing_id}, {self.member_id}, {self.amount_due}, {self.status}, {self.payment_method})"

    
