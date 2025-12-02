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
        return member
    else:
        print("Member not found. Please register first.")
        return None

def view_members(session: Session):
    members = session.query(Member).all()
    for member in members:
        print(member)

def update_personal_details(session: Session, member: Member, name=None, date_of_birth=None, gender=None, contact=None):
    changed = False
    if name:
        member.name = name
        changed = True
    if date_of_birth:
        if date_of_birth != "":
            member.date_of_birth = date_of_birth
            changed = True
    if gender:
        member.gender = gender
        changed = True
    if contact:
        member.contact_detail = contact
        changed = True
    if changed:
        session.commit()


def view_fitness_goals(session: Session, member: Member):
    if not member:
        print("Member not found.")
        return

    for i, goal in enumerate(member.goals):
        print(f"Goal {i + 1}: {goal.goal_type.description} (target: {goal.goal_type.target})")

def add_fitness_goals(session: Session, member: Member, description: str, target: str):
    if not member:
        print("Member not found.")
        return
    
    goal_type = GoalType(description=description, target=target)
    session.add(goal_type)
    session.flush()

    goal = HealthGoal(member=member, goal_type=goal_type)
    session.add(goal)
    session.commit()

def update_fitness_goals(session: Session, user_index: int, member: Member, goal_id: int, target: str):
    if not member:
        print("Member not found.")
        return
    if user_index - 1 >= len(member.goals):
        print("Goal index out of range.")
        return
    
    goal = member.goals[user_index - 1]
    goal.goal_type.target = target
    session.commit()
    
def input_health_metric(session: Session, member: Member, date_recorded: date, weight: float, height: float, heart_rate: int):
    if not member:
        print("Member not found.")
        return
    
    healthMetric = HealthMetric(member=member, date_recorded=date_recorded, weight=weight, height=height, heart_rate=heart_rate)
    session.add(healthMetric)
    session.commit()

def dashboard(session: Session, member: Member) -> None:
    if not member:
        print("Member not found.")
        return
    now = datetime.now()

    # 1) Latest 5 health stats (most recent first)
    latest_metrics = sorted(member.health_metrics, key=lambda m: m.date_recorded, reverse=True)[:5]

    # 2) Active goals (all HealthGoal rows for this member, joined to GoalType for details)
    active_goals = []
    for goal in member.goals:
        active_goals.append((goal, goal.goal_type))

    # 3) Past class count:
    #    GroupMember → FitnessClass → RoomBooking, where the booking has already ended
    past_class_count = 0
    for group_member in member.group_classes:
        if group_member.fitness_class.booking.end_time < now:
            past_class_count += 1

    # 4) Upcoming sessions:
    #    TrainingSession for this member, with a RoomBooking whose start_time is in the future
    upcoming_sessions = []
    for training_session in member.training_sessions:
        if training_session.booking.start_time >= now:
            upcoming_sessions.append(training_session)
    upcoming_sessions.sort(key=lambda training_session: training_session.booking.start_time)

    # 5) Upcoming group classes:
    #    GroupMember → FitnessClass → RoomBooking (+ Trainer), where start_time is in the future
    upcoming_classes = []
    for group_member in member.group_classes:
        if group_member.fitness_class.booking.start_time >= now:
            upcoming_classes.append(group_member.fitness_class)
    upcoming_classes.sort(key=lambda fc: fc.booking.start_time)
    
    # ==== PRINT DASHBOARD (terminal UI can format this however you like) ====
    print("\n====== DASHBOARD ======")

    print("\nLatest Health Metrics (up to 5, most recent first):")
    if not latest_metrics:
        print("  No health metrics recorded yet.")
    else:
        for metric in latest_metrics:
            print(
                f"  Date: {metric.date_recorded}, "
                f"Weight: {metric.weight}, "
                f"Height: {metric.height}, "
                f"Heart rate: {metric.heart_rate}"
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
        for training_session in upcoming_sessions:
            print(
                f"  {training_session.booking.start_time}–{training_session.booking.end_time} "
                f"with {training_session.trainer.name} (session_id={training_session.session_id})"
            )

    print("\nUpcoming Group Classes:")
    if not upcoming_classes:
        print("  No upcoming classes.")
    else:
        for fitness_class in upcoming_classes:
            print(
                f"  {fitness_class.booking.start_time}–{fitness_class.booking.end_time} "
                f"{fitness_class.class_name} with {fitness_class.trainer.name} "
                f"(class_id={fitness_class.class_id})"
            )
    print("=======================\n")
    return


# DEFAULT_ADMIN_ID_FOR_BOOKINGS = 1  # adjust if needed

def view_room_bookings(session: Session):
    bookings = session.query(RoomBooking).order_by(RoomBooking.start_time.asc()).all()
    #If no bookings found
    if not bookings:
        print("No room bookings found in the specified time range.")
        return

    for booking in bookings:
        print(
            f"Booking ID: {booking.booking_id}, "
            f"Room: {booking.room.room_name}, "
            f"Booked: {booking.is_booked}, "
            f"Start: {booking.start_time}, "
            f"End: {booking.end_time}"
        )

def view_pt_sessions(session: Session, member: Member):
    pt_sessions = session.query(TrainingSession).filter(TrainingSession.member == member).all()
    if not pt_sessions:
        print("No PT sessions found.")
        return
    pt_sessions.sort(key=lambda ts: ts.booking.start_time)

    for training_session in pt_sessions:
        print(
            f"Session ID: {training_session.session_id}, "
            f"Trainer: {training_session.trainer.name}, "
            f"Start: {training_session.booking.start_time}, "
            f"End: {training_session.booking.end_time}"
        )

def reschedule_pt_session(session: Session, member: Member, training_session: TrainingSession, new_booking: RoomBooking, new_trainer: Trainer = None):
    if not member:
        print("Member not found.")
        return None
    if not training_session or training_session.member != member:
        print("PT session not found for this member.")
        return None
    if not new_booking:
        print("New booking not found.")
        return None

    # Choose which trainer to use
    trainer = new_trainer if new_trainer is not None else training_session.trainer
    if not trainer:
        print("Trainer not found.")
        return None

    desired_start = new_booking.start_time
    desired_end = new_booking.end_time

    # Check trainer availability for the new time window
    for availability in trainer.availability:
        if availability.start_time <= desired_start and availability.end_time >= desired_end:
            break
    else:
        print("Trainer is not available for the new booking time.")
        return None

    # Check for conflicts with other PT sessions (exclude the session being rescheduled)
    for other_ts in trainer.sessions:
        if other_ts.session_id == training_session.session_id:
            continue
        other = other_ts.booking
        if other.start_time < desired_end and other.end_time > desired_start:
            print("Trainer already has another PT session at that time.")
            return None

    # Check for conflicts with fitness classes
    for fitness_class in trainer.classes:
        other = fitness_class.booking
        if other.start_time < desired_end and other.end_time > desired_start:
            print("Trainer is teaching a class at that time.")
            return None

    # All checks passed → update the session's booking and trainer (if changed)
    training_session.booking = new_booking
    training_session.trainer = trainer
    session.commit()
    print("PT session rescheduled successfully.")
    return training_session

def book_pt_session(session: Session, member: Member, trainer: Trainer, booking: RoomBooking):
    if not member or not trainer or not booking:
        print("Member, Trainer or Booking not found")
        return None

    # 3) Use booking's time window as the PT session time
    desired_start = booking.start_time
    desired_end = booking.end_time

    # 4) Check trainer availability for that whole time window
    for availability in trainer.availability:
        if availability.start_time <= desired_start and availability.end_time >= desired_end:
            break
    else:
        print("Trainer is not available for that booking time.")
        return None

    # 5) Check for conflicts with other PT sessions
    for training_session in trainer.sessions:
        other = training_session.booking
        if other.start_time < desired_end and other.end_time > desired_start:
            print("Trainer already has another PT session at that time.")
            return None

    # 6) Check for conflicts with fitness classes
    for fitness_class in trainer.classes:
        other = fitness_class.booking
        if other.start_time < desired_end and other.end_time > desired_start:
            print("Trainer is teaching a class at that time.")
            return None

    # 7) All good → create the PT session tied to that booking
    pt_session = TrainingSession(trainer=trainer, booking=booking, member=member)

    session.add(pt_session)
    session.commit()
    print("PT session booked successfully.")
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

def class_registration(session: Session, member: Member, fitness_class: FitnessClass):     
    if not member or not fitness_class:
        print("Member or class not found.")
        return False

    if any(group_member.member == member for group_member in fitness_class.members):
        print("Member is already signed up for this class.")
        return False
    
    if fitness_class.num_signed_up >= fitness_class.capacity:
        print("Class is full.")
        return False

    fitness_class.num_signed_up += 1
    group_member = GroupMember(fitness_class=fitness_class, member=member)
    session.add(group_member)
    session.commit()
    return fitness_class
