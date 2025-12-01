from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, ForeignKey, Numeric, PrimaryKeyConstraint, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from datetime import date, datetime

# Define Table Classes
Base = declarative_base()

# Schemas
class Member(Base):
    __tablename__ = "Member"

    # Columns
    member_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    date_of_birth: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    gender: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    contact_detail: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    # Relationships
    health_metrics: Mapped[list["HealthMetric"]] = relationship("HealthMetric", back_populates="member", cascade="all, delete-orphan")
    payments: Mapped[list["BillingPayment"]] = relationship("BillingPayment", back_populates="member", cascade="all, delete-orphan")
    goals: Mapped[list["HealthGoal"]] = relationship("HealthGoal", back_populates="member", cascade="all, delete-orphan")
    group_classes: Mapped[list["GroupMember"]] = relationship("GroupMember", back_populates="member", cascade="all, delete-orphan" )
    training_sessions: Mapped[list["TrainingSession"]] = relationship("TrainingSession", back_populates="member", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Member({self.member_id}, {self.name!r}, {self.date_of_birth}, {self.gender!r}, {self.contact_detail!r})"

class HealthMetric(Base):
    __tablename__ = "HealthMetric"

    # Columns
    metric_id: Mapped[int] = mapped_column(primary_key=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("Member.member_id"), nullable=False)
    date_recorded: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    weight: Mapped[Optional[float]] = mapped_column(Numeric(5, 2), nullable=True)
    height: Mapped[Optional[float]] = mapped_column(Numeric(5, 2), nullable=True)
    heart_rate: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Relationships
    member: Mapped["Member"] = relationship("Member", back_populates="health_metrics")

    def __repr__(self) -> str:
        return (f"HealthMetric({self.metric_id}, member_id={self.member_id}, "f"date={self.date_recorded}, weight={self.weight}, height={self.height}, hr={self.heart_rate})")

class BillingPayment(Base):
    __tablename__ = "BillingPayment"

    # Columns
    billing_id: Mapped[int] = mapped_column(primary_key=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("Member.member_id"), nullable=False)
    type_of_billing: Mapped[str] = mapped_column(String(50), nullable=False)
    amount_due: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    payment_method: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # Relationship
    member: Mapped["Member"] = relationship("Member", back_populates="payments")

    def __repr__(self) -> str:
        return f"BillingPayment({self.billing_id}, member={self.member_id}, {self.amount_due}, {self.status})"

class GoalType(Base):
    __tablename__ = "GoalType"

    # Columns
    goal_type_id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(50), nullable=False)
    target: Mapped[str] = mapped_column(String(50), nullable=False)

    # Relationships
    goals: Mapped[list["HealthGoal"]] = relationship("HealthGoal", back_populates="goal_type", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"GoalType({self.goal_type_id}, {self.description!r}, {self.target!r})"

class HealthGoal(Base):
    __tablename__ = "HealthGoal"

    # Columns 
    goal_id: Mapped[int] = mapped_column(primary_key=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("Member.member_id"), nullable=False)
    goal_type_id: Mapped[int] = mapped_column(ForeignKey("GoalType.goal_type_id"), nullable=False)

    # Relationships
    member: Mapped["Member"] = relationship("Member", back_populates="goals")
    goal_type: Mapped["GoalType"] = relationship("GoalType", back_populates="goals")

    def __repr__(self) -> str:
        return f"HealthGoal({self.goal_id}, member={self.member_id}, type={self.goal_type_id})"

class Admin(Base):
    __tablename__ = "Admin"

    # Columns
    admin_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

    # Relationships
    equipment_operations: Mapped[list["EquipmentManagement"]] = relationship("EquipmentManagement", back_populates="admin", cascade="all, delete-orphan")
    room_bookings: Mapped[list["RoomBooking"]] = relationship("RoomBooking", back_populates="admin", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Admin({self.admin_id}, {self.name!r})"

class EquipmentManagement(Base):
    __tablename__ = "EquipmentManagement"

    # Columns
    equipment_id: Mapped[int] = mapped_column(primary_key=True)
    admin_id: Mapped[int] = mapped_column(ForeignKey("Admin.admin_id"), nullable=False)
    admin_operation: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)

    # Relationship
    admin: Mapped["Admin"] = relationship("Admin", back_populates="equipment_operations")

    def __repr__(self) -> str:
        return f"Equipment({self.equipment_id}, admin={self.admin_id}, op={self.admin_operation!r}, status={self.status!r}1)"

class Room(Base):
    __tablename__ = "Room"

    # Columns
    room_id: Mapped[int] = mapped_column(primary_key=True)
    room_name: Mapped[str] = mapped_column(String(50), nullable=False)

    # Relationship
    bookings: Mapped[list["RoomBooking"]] = relationship("RoomBooking", back_populates="room", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Room({self.room_id}, {self.room_name!r})"

class RoomBooking(Base):
    __tablename__ = "RoomBooking"

    # Columns
    booking_id: Mapped[int] = mapped_column(primary_key=True)
    admin_id: Mapped[int] = mapped_column(ForeignKey("Admin.admin_id"), nullable=False)
    room_id: Mapped[int] = mapped_column(ForeignKey("Room.room_id"), nullable=False)
    is_booked: Mapped[bool] = mapped_column(Boolean, nullable=False)
    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    # Relationships
    admin: Mapped["Admin"] = relationship("Admin", back_populates="room_bookings")
    room: Mapped["Room"] = relationship("Room", back_populates="bookings")
    fitness_classes: Mapped[list["FitnessClass"]] = relationship("FitnessClass", back_populates="booking", cascade="all, delete-orphan")
    training_sessions: Mapped[list["TrainingSession"]] = relationship("TrainingSession", back_populates="booking", cascade="all, delete-orphan")

    # Index
    __table_args__ = (
        Index("ix_roombooking_room_time", "room_id", "start_time", "end_time"),
    )

    def __repr__(self) -> str:
        return f"RoomBooking({self.booking_id}, room={self.room_id}, {self.start_time}–{self.end_time})"

class Trainer(Base):
    __tablename__ = "Trainer"

    # Columns
    trainer_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    # Relationships
    classes: Mapped[list["FitnessClass"]] = relationship("FitnessClass", back_populates="trainer", cascade="all, delete-orphan" )
    availability: Mapped[list["Availability"]] = relationship("Availability", back_populates="trainer", cascade="all, delete-orphan")
    sessions: Mapped[list["TrainingSession"]] = relationship("TrainingSession", back_populates="trainer", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Trainer({self.trainer_id}, {self.name!r})"

class FitnessClass(Base):
    __tablename__ = "FitnessClass"

    # Columns
    class_id: Mapped[int] = mapped_column(primary_key=True)
    trainer_id: Mapped[int] = mapped_column(ForeignKey("Trainer.trainer_id"), nullable=False)
    booking_id: Mapped[int] = mapped_column(ForeignKey("RoomBooking.booking_id"), nullable=False)
    class_name: Mapped[str] = mapped_column(String(50), nullable=False)
    capacity: Mapped[int] = mapped_column(nullable=False)
    num_signed_up: Mapped[int] = mapped_column(default=0, nullable=False)

    # Relationships
    trainer: Mapped["Trainer"] = relationship("Trainer", back_populates="classes")
    booking: Mapped["RoomBooking"] = relationship("RoomBooking", back_populates="fitness_classes")
    members: Mapped[list["GroupMember"]] = relationship("GroupMember", back_populates="fitness_class", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"FitnessClass({self.class_id}, {self.class_name!r}, signed_up={self.num_signed_up}/{self.capacity})"

class GroupMember(Base):
    __tablename__ = "GroupMember"

    # Columns
    class_id: Mapped[int] = mapped_column(ForeignKey("FitnessClass.class_id"), nullable=False)
    member_id: Mapped[int] = mapped_column(ForeignKey("Member.member_id"), nullable=False)

    # Relationhips
    fitness_class: Mapped["FitnessClass"] = relationship("FitnessClass", back_populates="members")
    member: Mapped["Member"] = relationship("Member", back_populates="group_classes")

    # Composite key
    __table_args__ = (
        PrimaryKeyConstraint("class_id", "member_id"),
    )

    def __repr__(self) -> str:
        return f"GroupMember(class={self.class_id}, member={self.member_id})"

class Availability(Base):
    __tablename__ = "Availability"

    # Columns
    availability_id: Mapped[int] = mapped_column(primary_key=True)
    trainer_id: Mapped[int] = mapped_column(ForeignKey("Trainer.trainer_id"), nullable=False)
    is_recurring: Mapped[bool] = mapped_column(Boolean, nullable=False)
    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    # Relationship
    trainer: Mapped["Trainer"] = relationship("Trainer", back_populates="availability")

    def __repr__(self) -> str:
        return f"Availability(trainer={self.trainer_id}, {self.start_time}–{self.end_time}, recurring={self.is_recurring})"

class TrainingSession(Base):
    __tablename__ = "TrainingSession"

    # Columns
    session_id: Mapped[int] = mapped_column(primary_key=True)
    trainer_id: Mapped[int] = mapped_column(ForeignKey("Trainer.trainer_id"), nullable=False)
    booking_id: Mapped[int] = mapped_column(ForeignKey("RoomBooking.booking_id"), nullable=False)
    member_id: Mapped[int] = mapped_column(ForeignKey("Member.member_id"), nullable=False)

    # Relationships
    trainer: Mapped["Trainer"] = relationship("Trainer", back_populates="sessions")
    booking: Mapped["RoomBooking"] = relationship("RoomBooking", back_populates="training_sessions")
    member: Mapped["Member"] = relationship("Member", back_populates="training_sessions")

    def __repr__(self) -> str:
        return f"TrainingSession({self.session_id}, trainer={self.trainer_id}, member={self.member_id})"