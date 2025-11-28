from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, ForeignKey, Numeric, PrimaryKeyConstraint
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
    contact_detail = Column(String(255), nullable=False, unique=True)

    #Print statement
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

    #Print statement
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

    #Print statement
    def __repr__(self):
        return f"({self.billing_id}, {self.member_id}, {self.amount_due}, {self.status}, {self.payment_method})"

#Health goal Table
class HealthGoal(Base):
    __tablename__ = "HealthGoal"
    goal_id = Column(Integer, primary_key=True)
    member_id = Column(Integer, ForeignKey('Member.member_id'), nullable = False)
    goal_type_id = Column(Integer, ForeignKey('GoalType.goal_type_id'), nullable = False)

    #Print statement
    def __repr__(self):
        return f"({self.goal_id}, {self.member_id}, {self.goal_type_id})"

    #member_id = Column(Integer, ForeignKey('Member.member_id'), nullable=False)

'''
CREATE TABLE HealthGoal (
    goal_id      INT PRIMARY KEY,
    member_id    INT NOT NULL,
    goal_type_id INT NOT NULL,
    FOREIGN KEY (member_id)    REFERENCES Member(member_id),
    FOREIGN KEY (goal_type_id) REFERENCES GoalType(goal_type_id)
);
'''
class GoalType(Base):
    __tablename__ = "GoalType"
    goal_type_id = Column(Integer, primary_key=True, nullable = False)
    description = Column(String(50), nullable = False)
    target = Column(String(50), nullable = False)
    
"""
-- GOAL TYPE
CREATE TABLE GoalType (
    goal_type_id INT PRIMARY KEY,
    description  VARCHAR(255),
    target       VARCHAR(255)
);
"""
#Admin Table
class Admin(Base):
    __tablename__ = "Admin"
    admin_id = Column(Integer, primary_key=True, nullable = False)
    name = Column(String(50), nullable = False)

    #Print statement
    def __repr__(self):
        return f"({self.admin_id}, {self.name})"
    
#Equipment Management Table
class EquipmentMangement(Base):
    __tablename__ = "EquipmentManagement"
    equipment_id = Column(Integer, primary_key=True, nullable = False)
    admin_id = Column(Integer, ForeignKey('Admin.admin_id'), nullable = False)
    admin_operation = Column(String(100), nullable = False)
    status = Column(String(50), nullable = False)

    #Print statement
    def __repr__(self):
        return f"({self.equipment_id}, {self.admin_id}, {self.admin_operation}, {self.status})"

"""
-- ADMIN
CREATE TABLE Admin (
    admin_id INT PRIMARY KEY,
    name     VARCHAR(100) NOT NULL
);
"""
class Room(Base):
    __tablename__ = "Room"
    room_id = Column(Integer, primary_key=True, nullable = False)
    room_name = Column(String(50), nullable = False)
    
    #Print statement
    def __repr__(self):
        return f"({self.room_id}, {self.room_name})"

"""
-- ROOM
CREATE TABLE Room (
    room_id   INT PRIMARY KEY,
    room_name VARCHAR(100) NOT NULL
);
"""
class RoomBooking(Base):
    __tablename__ = "RoomBooking"
    booking_id = Column(Integer, primary_key = True, nullable = False)
    admin_id = Column(Integer, ForeignKey('Admin.admin_id'), nullable = False)
    room_id = Column(Integer, ForeignKey('Room.room_id'), nullable = False)
    is_booked = Column(Boolean, nullable = False)
    start_time = Column(DateTime, nullable = False)
    end_time = Column(DateTime, nullable = False)

    #Print statement
    def __repr__(self):
        return f"({self.booking_id}, {self.admin_id}, {self.room_id}, {self.is_booked}, {self.start_time}, {self.end_time})"
"""
-- ROOM BOOKING
CREATE TABLE RoomBooking (
    booking_id INT PRIMARY KEY,
    admin_id   INT NOT NULL,
    room_id    INT NOT NULL,
    is_booked  BOOLEAN,
    FOREIGN KEY (admin_id) REFERENCES Admin(admin_id),
    FOREIGN KEY (room_id)  REFERENCES Room(room_id)
);
"""

#Trainer Table
class Trainer(Base):
    __tablename__ = "Trainer"
    trainer_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    #Print statement
    def __repr__(self):
        return f"({self.trainer_id}, {self.name})"
        
#Fitness Class Table
class FitnessClass(Base):
    __tablename__ = "FitnessClass"
    class_id = Column(Integer, primary_key=True)
    trainer_id = Column(Integer, ForeignKey('Trainer.trainer_id'), nullable=False)
    booking_id = Column(Integer, ForeignKey('RoomBooking.booking_id'), nullable=False)
    class_name = Column(String(50), nullable=False)
    capacity = Column(Integer, nullable=False)

    #Print statement
    def __repr__(self):
        return f"({self.class_id}, {self.trainer_id}, {self.booking_id}, {self.class_name}, {self.capacity})"
    
#Group Members Table
class GroupMember(Base):
    __tablename__ = "GroupMember"
    class_id = Column(Integer, ForeignKey('FitnessClass.class_id'), nullable=False)
    member_id = Column(Integer, ForeignKey('Member.member_id'), nullable=False)
    __table_args__ = (
        PrimaryKeyConstraint('class_id', 'member_id'),
    )
    #Print statement
    def __repr__(self):
        return f"({self.class_id}, {self.member_id})"

#Availability Table
class Availability(Base):
    __tablename__ = "Availability"
    availability_id = Column(Integer, primary_key=True)
    trainer_id = Column(Integer, ForeignKey('Trainer.trainer_id'), nullable=False)
    is_recurring = Column(Boolean, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)

    #Print statement
    def __repr__(self):
        return f"({self.trainer_id}, {self.is_recurring}, {self.start_time}, {self.end_time})"

#Training Session Table
class TrainingSession(Base):
    __tablename__ = "TrainingSession"
    session_id = Column(Integer, primary_key=True)
    trainer_id = Column(Integer, ForeignKey('Trainer.trainer_id'), nullable=False)
    booking_id = Column(Integer, ForeignKey('RoomBooking.booking_id'), nullable=False)
    member_id = Column(Integer, ForeignKey('Member.member_id'), nullable=False)

    #Print statement
    def __repr__(self):
        return f"({self.session_id}, {self.trainer_id}, {self.booking_id}, {self.member_id})"


