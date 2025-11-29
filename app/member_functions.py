from sqlalchemy.orm import Session
from sqlalchemy import Numeric, text
import sys, os
from datetime import date, datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.schemas import Member, GoalType, HealthMetric, HealthGoal, TrainingSession, RoomBooking, GroupMember, FitnessClass, Trainer, Availability, Room

def register_member(session: Session, name: str, date_of_birth: date, gender: str, contact_detail: str):
    existing_member = session.query(Member).filter_by(contact_detail=contact_detail).first()
    if existing_member:
        print("Error: contact details must be unique!")
    else:
        member = Member(name=name, date_of_birth=date_of_birth, gender=gender, contact_detail=contact_detail)
        session.add(member)
        session.commit()
        print(f"{name} has successfully been registered as a member.")

def login_member(session: Session, name: str):
    member = session.query(Member).filter(Member.name == name).first()
    if member:
        print(f"Welcome back, {member.name}!")
        return member.member_id
    else:
        print("Member not found. Please register first.")
        return None
    
def view_members(session: Session):
    members = session.query(Member).all()
    for member in members:
        print(member)

def update_personal_details(session: Session, id: int, name="null", date_of_birth = "null", gender = "null", contact = "null"):

    changed = False
    member = session.query(Member).filter(Member.member_id == id).first()
    if(name != "null"):
        member.name = name
        changed = True
    if(date_of_birth != "null"):
        member.date_of_birth = date_of_birth
        changed = True
    if(gender != "null"):
        member.gender = gender
        changed = True
    if(contact != "null"):
        member.contact_detail = contact
        changed = True
    if(changed == True):
        session.commit()
    return

def view_fitness_goals(session: Session, member_id: int):
    goals = session.query(HealthGoal).filter(HealthGoal.member_id == member_id).all()
    for i, goal in enumerate(goals):
        goal_type = session.query(GoalType).filter(GoalType.goal_type_id == goal.goal_type_id).first()
        print(f"Goal {i + 1}: {goal_type.description} (target: {goal_type.target})")

def add_fitness_goals(session: Session, member_id: int, description: str, target: str):
    goal_type = GoalType(description=description, target=target)
    session.add(goal_type)
    session.flush()
    goal_type_id = goal_type.goal_type_id
    goal = HealthGoal(member_id=member_id, goal_type_id=goal_type_id)
    session.add(goal)
    session.commit()

def update_fitness_goals(session: Session, user_index: int, member_id:int, goal_id: int, target: str):
    goal = session.query(HealthGoal).filter(HealthGoal.member_id == member_id).all()[user_index - 1]
    goal_type = session.query(GoalType).filter(GoalType.goal_type_id == goal.goal_type_id).first() 
    goal_type.target = target
    session.commit()
    
def input_health_metric(session: Session, member_id: int, date_recorded: date, weight: float, height: float, heart_rate: int):
    healthMetric = HealthMetric(member_id=member_id, date_recorded=date_recorded, weight=weight, height=height, heart_rate=heart_rate)
    session.add(healthMetric)
    session.commit()

def dashboard(session: Session, member_id: int) -> None:
    now = datetime.now()

    # 1) Latest health stats (most recent HealthMetric row for this member)
    latest_metric = (
        session.query(HealthMetric)
        .filter(HealthMetric.member_id == member_id)
        .order_by(HealthMetric.date_recorded.desc())
        .first()
    )

    # 2) Active goals (all HealthGoal rows for this member, joined to GoalType for details)
    active_goals = (
        session.query(HealthGoal, GoalType)
        .join(GoalType, HealthGoal.goal_type_id == GoalType.goal_type_id)
        .filter(HealthGoal.member_id == member_id)
        .all()
    )

    # 3) Past class count:
    #    GroupMember → FitnessClass → RoomBooking, where the booking has already ended
    past_class_count = (
        session.query(GroupMember)
        .join(FitnessClass, GroupMember.class_id == FitnessClass.class_id)
        .join(RoomBooking, FitnessClass.booking_id == RoomBooking.booking_id)
        .filter(
            GroupMember.member_id == member_id,
            RoomBooking.end_time < now
        )
        .count()
    )

    # 4) Upcoming sessions:
    #    TrainingSession for this member, with a RoomBooking whose start_time is in the future
    upcoming_sessions = (
        session.query(TrainingSession, RoomBooking, Trainer)
        .join(RoomBooking, TrainingSession.booking_id == RoomBooking.booking_id)
        .join(Trainer, TrainingSession.trainer_id == Trainer.trainer_id)
        .filter(
            TrainingSession.member_id == member_id,
            RoomBooking.start_time >= now
        )
        .order_by(RoomBooking.start_time.asc())
        .all()
    )

    # ==== PRINT DASHBOARD (terminal UI can format this however you like) ====
    print("\n====== DASHBOARD ======")

    print("\nLatest Health Stats:")
    if latest_metric is None:
        print("  No health metrics recorded yet.")
    else:
        print(
            f"  Date: {latest_metric.date_recorded}, "
            f"Weight: {latest_metric.weight}, "
            f"Height: {latest_metric.height}, "
            f"Heart rate: {latest_metric.heart_rate}"
        )

    print("\nActive Goals:")
    if not active_goals:
        print("  No goals set.")
    else:
        for goal, goaltype in active_goals:
            print(f"  {goaltype.description} (target: {goaltype.target})")

    print(f"\nPast class count: {past_class_count}")

    print("\nUpcoming Sessions:")
    if not upcoming_sessions:
        print("  No upcoming sessions.")
    else:
        for ts, booking, trainer in upcoming_sessions:
            print(
                f"  {booking.start_time}–{booking.end_time} "
                f"with {trainer.name} (session_id={ts.session_id})"
            )

    print("=======================\n")
    return


# DEFAULT_ADMIN_ID_FOR_BOOKINGS = 1  # adjust if needed

def view_room_bookings(session: Session, start_time: datetime, end_time: datetime):
    bookings = (session.query(RoomBooking, Room).join(Room, RoomBooking.room_id == Room.room_id).filter().order_by(RoomBooking.start_time.asc()).all())

    #If no bookings found
    if not bookings:
        print("No room bookings found in the specified time range.")
        return

    for booking, room in bookings:
        print(
            f"Booking ID: {booking.booking_id}, "
            f"Room: {room.room_name}, "
            f"Booked: {booking.is_booked}, "
            f"Start: {booking.start_time}, "
            f"End: {booking.end_time}"
        )

def view_pt_sessions(session: Session, member_id: int):
    sessions = (
        session.query(TrainingSession, RoomBooking, Trainer)
        .join(RoomBooking, TrainingSession.booking_id == RoomBooking.booking_id)
        .join(Trainer, TrainingSession.trainer_id == Trainer.trainer_id)
        .filter(TrainingSession.member_id == member_id)
        .order_by(RoomBooking.start_time.asc())
        .all()
    )

    if not sessions:
        print("No PT sessions found.")
        return

    for ts, booking, trainer in sessions:
        print(
            f"Session ID: {ts.session_id}, "
            f"Trainer: {trainer.name}, "
            f"Start: {booking.start_time}, "
            f"End: {booking.end_time}"
        )

def book_pt_session(session: Session, member_id: int, trainer_id: int, start_time: datetime, end_time: datetime, booking_id: int):
    
    trainer = session.query(Trainer).filter(Trainer.trainer_id == trainer_id).first()
    if trainer is None:
        print("Trainer not found.")
        return None

    # resolve time window (from booking if given, else from args)
    if booking_id is not None:
        booking = (session.query(RoomBooking).filter(RoomBooking.booking_id == booking_id).first())
        if booking is None:
            print("Booking not found.")
            return None
        desired_start, desired_end = booking.start_time, booking.end_time
    else:
        print("No booking ID provided")
        return None

    if desired_end <= desired_start:
        print("End time must be after start time.")
        return None

    # within availability?
    availability = (
        session.query(Availability)
        .filter(
            Availability.trainer_id == trainer_id,
            Availability.start_time <= desired_start,
            Availability.end_time >= desired_end,
        ).first()
    )
    if availability is None:
        print("Time not within trainer availability.")
        return None

    # no trainer conflict in pt sessions
    trainer_pt_conflict = (
        session.query(TrainingSession)
        .join(RoomBooking, TrainingSession.booking_id == RoomBooking.booking_id)
        .filter(
            TrainingSession.trainer_id == trainer_id,
            RoomBooking.start_time < desired_end,
            RoomBooking.end_time > desired_start,
        )
        .first()
    )
    if trainer_pt_conflict is not None:
        print("Trainer has another session at that time.")
        return None

    # no trainer conflict in classes
    trainer_class_conflict = (
        session.query(FitnessClass)
        .join(RoomBooking, FitnessClass.booking_id == RoomBooking.booking_id)
        .filter(
            FitnessClass.trainer_id == trainer_id,
            RoomBooking.start_time < desired_end,
            RoomBooking.end_time > desired_start,
        )
        .first()
    )
    if trainer_class_conflict is not None:
        print("Trainer has another class at that time.")
        return None
    
    pt_session = TrainingSession(trainer_id=trainer_id, booking_id=booking.booking_id, member_id=member_id)
    session.add(pt_session)
    session.commit()
    return pt_session

def view_available_classes(session: Session):
    #Try to use view first
    try:
        result = session.execute(text("SELECT * FROM view_available_classes ORDER BY class_name ASC"))
        rows = result.fetchall()
        if not rows:
            print("No available classes.")
            return
        keys = result.keys()
        for row in rows:
            if hasattr(row, '_mapping'):
                mapping = row._mapping
            else:
                mapping = dict(zip(keys, row))
            print(f"Class ID: {mapping.get('class_id')}, Trainer ID: {mapping.get('trainer_id')}, Booking ID: {mapping.get('booking_id')}, Name: {mapping.get('class_name')}, Capacity: {mapping.get('num_signed_up')}/{mapping.get('capacity')}")
        return
    except Exception as e:
        print("View not available or failed; falling back to table query.", e)

    #Backup: direct table query
    classes = session.query(FitnessClass).order_by(FitnessClass.class_name.asc()).all()
    for fitness_class in classes:
        print(fitness_class)

def class_registration(session: Session, member_id: int, class_id: int): 
    fitness_class = session.query(FitnessClass).filter(FitnessClass.class_id == class_id).first()
    if fitness_class is None:
        print("Class not found.")
        return False

    already = session.query(GroupMember).filter(GroupMember.class_id == class_id, GroupMember.member_id == member_id).first()
    if already:
        print("Member is already signed up for this class.")
        return False

    if fitness_class.num_signed_up >= fitness_class.capacity:
        print("Class is full.")
        return False

    fitness_class.num_signed_up += 1
    group_member = GroupMember(class_id=class_id, member_id=member_id)
    session.add(group_member)
    session.commit()
    return fitness_class
