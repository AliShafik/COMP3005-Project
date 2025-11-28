from sqlalchemy.orm import Session
import sys, os
import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.schemas import Room, RoomBooking, EquipmentMangement, FitnessClass, BillingPayment

def room_booking(session: Session, admin_id: int, room_name: str, start_date: str, start_time: str, end_date: str, end_time: str):
    # - date in "YYYY-MM-DD"
    # - time in "HH:MM"
    start_dt = datetime.datetime.strptime(f"{start_date} {start_time}", "%Y-%m-%d %H:%M")
    end_dt = datetime.datetime.strptime(f"{end_date} {end_time}", "%Y-%m-%d %H:%M")

    # check if room exists, if not create it
    room = session.query(Room).filter(Room.room_name == room_name).first()
    if not room:
        room = Room(room_name = room_name)
        session.add(room)
        session.flush()

    # simple overlap check for existing bookings
    conflict = session.query(RoomBooking).filter(
        RoomBooking.room_id == room.room_id,
        RoomBooking.is_booked == True,
        RoomBooking.start_time < end_dt,
        RoomBooking.end_time > start_dt,
    ).first()
    if conflict:
        return None

    rb = RoomBooking(admin_id = admin_id, room_id = room.room_id, is_booked = True, start_time = start_dt, end_time = end_dt)
    session.add(rb)
    session.commit()
    return rb

def equipment_maintenance(session: Session, admin_id: int, operation: str, status = "open"):
    em = EquipmentMangement(admin_id = admin_id, admin_operation = operation, status = status)
    session.add(em)
    session.commit()
    return em

def class_management(session: Session, admin_id: int, trainer_id: int, class_name: str, capacity: int, room_name: str, start_date: str, start_time: str, end_date: str, end_time: str):
    rb = room_booking(session, admin_id, room_name, start_date, start_time, end_date, end_time)
    if not rb:
        return None
    fc = FitnessClass(trainer_id = trainer_id, booking_id = rb.booking_id, class_name = class_name, capacity = capacity)
    session.add(fc)
    session.commit()
    return fc

def billing_and_payments(session: Session, action = "create", member_id = None, type_of_billing = None, amount = None, billing_id = None, payment_method = None):
    if action == "create":
        bp = BillingPayment(member_id = member_id, type_of_billing = type_of_billing, amount_due = amount, status = "due")
        session.add(bp)
        session.commit()
        return bp
    elif action == "pay":
        bp = session.query(BillingPayment).filter(BillingPayment.billing_id == billing_id).first()
        if not bp:
            return None
        bp.payment_method = payment_method
        bp.status = "paid"
        session.commit()
        return bp
    return None
