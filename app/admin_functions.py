from sqlalchemy.orm import Session
import sys, os
import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.schemas import Room, RoomBooking, EquipmentManagement, FitnessClass, BillingPayment, Admin, Trainer, Member

#Admin Management

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
        return admin
    else:
        print("Admin not found. Please register first.")
        return None
    
def view_admins(session: Session):
    admins = session.query(Admin).all()
    for admin in admins:
        print(admin)

# Room Management

def view_rooms(session: Session):
    rooms = session.query(Room).all()
    for room in rooms:
        print(room)

def view_room_bookings(session: Session):
    bookings = session.query(RoomBooking).all()
    for booking in bookings:
        print(booking)

def room_booking(session: Session, admin: Admin, room_name: str, start_date: str, start_time: str, end_date: str, end_time: str):
    # - date in "YYYY-MM-DD"
    # - time in "HH:MM"
    start_dt = datetime.datetime.strptime(f"{start_date} {start_time}", "%Y-%m-%d %H:%M")
    end_dt = datetime.datetime.strptime(f"{end_date} {end_time}", "%Y-%m-%d %H:%M")

    room = session.query(Room).filter(Room.room_name == room_name).first()
    if not room:
        room = Room(room_name = room_name)
        session.add(room)
        session.flush()

    for booking in room.bookings:
        if booking.is_booked and booking.start_time < end_dt and booking.end_time > start_dt:
            return None

    booking = RoomBooking(admin = admin, room = room, is_booked = False, start_time = start_dt, end_time = end_dt)
    session.add(booking)
    session.commit()
    return booking

# Equipment Maintenance

def view_equipment_maintenance(admin: Admin):
    maintenances = sorted(admin.equipment_operations, key=lambda m: m.equipment_id, reverse=True)
    for maintenance in maintenances:
        print(maintenance)

def add_equipment_maintenance(session: Session, admin: Admin, operation: str, status = "open"):
    em = EquipmentManagement(admin = admin, admin_operation = operation, status = status)
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

# Fitness classes

def view_fitness_classes(session: Session):
    all_classes = []
    room_bookings = session.query(RoomBooking).all()
    for room_booking in room_bookings:
        for fitness_class in room_booking.fitness_classes:
            all_classes.append(fitness_class)
    all_classes.sort(key=lambda fitness_class: fitness_class.class_name)
    
    for fitness_class in all_classes:
        print(fitness_class)

def add_fitness_class(session: Session, admin: Admin, trainer: Trainer, class_name: str, capacity: int, room_name: str, start_date: str, start_time: str, end_date: str, end_time: str):
    if session.query(Room).filter(Room.room_name == room_name).first() is None:
        print("Error: Room not found.")
        return None
    rb = room_booking(session, admin, room_name, start_date, start_time, end_date, end_time)
    if not rb:
        print("Error: Room booking failed.")
        return None

    try:
        rb.is_booked = True
        session.flush()
    except Exception as e:
        session.rollback()
        print("Error marking room booking as booked:", e)
        return None
    
    if not trainer:
        print("Error: Trainer not found.")
        return None
    
    fc = FitnessClass(trainer = trainer, booking = rb, class_name = class_name, capacity = capacity, num_signed_up = 0)
    session.add(fc)
    session.commit()
    print(f"Fitness class '{class_name}' added successfully.")
    return fc

def billing_and_payments(session: Session, action="create", member: Member = None, type_of_billing=None, amount=None, billing_id=None, payment_method=None):
    if action == "create" and member:
        bp = BillingPayment(member=member, type_of_billing=type_of_billing, amount_due=amount, status="due")
        session.add(bp)
        session.commit()
        return bp
    elif action == "pay":
        bp = session.query(BillingPayment).filter_by(billing_id=billing_id).first()
        if not bp:
            return None
        bp.payment_method = payment_method
        bp.status = "paid"
        session.commit()
        return bp
    return None

def view_billings(session: Session):
    billings = session.query(BillingPayment).all()
    for billing in billings:
        print(billing)
