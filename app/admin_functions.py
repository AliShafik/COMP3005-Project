from sqlalchemy.orm import Session
import sys, os
import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.schemas import Room, RoomBooking, EquipmentManagement, FitnessClass, BillingPayment, Admin, Trainer

def register_admin(session: Session, name: str):
    existing_member = session.query(Admin).filter_by(name=name).first()
    if existing_member:
        print("Error: name must be unique!")
    else:
        admin = Admin(name=name)
        session.add(admin)
        session.commit()
        print(f"{name} has successfully been registered as a admin.")

def login_admin(session: Session, name: str):
    admin = session.query(Admin).filter(Admin.name == name).first()
    if admin:
        print(f"Welcome back, {admin.name}!")
        return admin.admin_id
    else:
        print("Admin not found. Please register first.")
        return None
    
def view_admins(session: Session):
    admins = session.query(Admin).all()
    for admin in admins:
        print(admin)

def view_rooms(session: Session):
    rooms = session.query(Room).all()
    for room in rooms:
        print(room)

def view_room_bookings(session: Session, admin_id: int):
    bookings = session.query(RoomBooking).filter(RoomBooking.admin_id == admin_id).order_by(RoomBooking.start_time.desc()).all()
    for booking in bookings:
        print(booking)

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
    conflict = session.query(RoomBooking).filter(RoomBooking.room_id == room.room_id, RoomBooking.is_booked == True, RoomBooking.start_time < end_dt, RoomBooking.end_time > start_dt, ).first()
    if conflict:
        return None

    rb = RoomBooking(admin_id = admin_id, room_id = room.room_id, is_booked = False, start_time = start_dt, end_time = end_dt)
    session.add(rb)
    session.commit()
    return rb

def view_equipment_maintenance(session: Session, admin_id: int):
    maintenances = session.query(EquipmentManagement).filter(EquipmentManagement.admin_id == admin_id).order_by(EquipmentManagement.equipment_id.desc()).all()
    for maintenance in maintenances:
        print(maintenance)

def add_equipment_maintenance(session: Session, admin_id: int, operation: str, status = "open"):
    em = EquipmentManagement(admin_id = admin_id, admin_operation = operation, status = status)
    session.add(em)
    session.commit()
    print(f"Equipment maintenance record created (id: {em.equipment_id})")

def edit_equipment_maintenance(session: Session, equipment_id: int, status: str):
    em = session.query(EquipmentManagement).filter(EquipmentManagement.equipment_id == equipment_id).first()
    if not em:
        print("Error: Equipment maintenance record not found.")
        return None
    em.status = status
    session.commit()
    print(f"Equipment maintenance record {equipment_id} updated.")

def view_fitness_classes(session: Session, admin_id: int):
    classes = session.query(FitnessClass).join(RoomBooking, FitnessClass.booking_id == RoomBooking.booking_id).filter(RoomBooking.admin_id == admin_id).order_by(FitnessClass.class_name.asc()).all()
    for fitness_class in classes:
        print(fitness_class)

def add_fitness_class(session: Session, admin_id: int, trainer_id: int, class_name: str, capacity: int, room_name: str, start_date: str, start_time: str, end_date: str, end_time: str):
    if session.query(Room).filter(Room.room_name == room_name).first() is None:
        print("Error: Room not found.")
        return None
    rb = room_booking(session, admin_id, room_name, start_date, start_time, end_date, end_time)
    if not rb:
        print("Error: Room booking failed.")
        return None

    try:
        rb_db = session.query(RoomBooking).filter(RoomBooking.booking_id == rb.booking_id).first()
        if rb_db is None:
            print("Error: Room booking record not found after creation.")
            return None
        rb_db.is_booked = True
        session.flush()
    except Exception as e:
        session.rollback()
        print("Error marking room booking as booked (possible overlap):", e)
        return None
    
    if session.query(Trainer).filter(Trainer.trainer_id == trainer_id).first() is None:
        print("Error: Trainer not found.")
        return None
    fc = FitnessClass(trainer_id = trainer_id, booking_id = rb.booking_id, class_name = class_name, capacity = capacity, num_signed_up = 0)
    session.add(fc)
    session.commit()
    print(f"Fitness class '{class_name}' added successfully.")

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
