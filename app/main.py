from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.schemas import Base, Member, Trainer, Admin, Room, TrainingSession, FitnessClass, RoomBooking, GroupMember, HealthGoal, GoalType, HealthMetric, BillingPayment, EquipmentManagement, Availability
from datetime import date, datetime, timedelta
import terminal_UI
import glob
from pathlib import Path

def reset_db(conn):
    conn.execute(text("""
        SELECT pg_terminate_backend(pid)
        FROM pg_stat_activity
        WHERE datname = current_database() AND pid <> pg_backend_pid();
    """))

    conn.execute(text("DROP SCHEMA public CASCADE;"))
    conn.execute(text("CREATE SCHEMA public;"))


def main():
    print("Starting Health & Fitness Club Management System...")

    #Connect to db (change to your own local db)
    engine = create_engine("postgresql://test:test@localhost:5432/project", echo=False)

    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            print("Database connection SUCCESSFUL")
    except Exception as e:
        print("Database connection FAILED:", e)

    #Create tables
    with engine.begin() as conn:
        reset_db(conn)
        Base.metadata.create_all(bind=conn)

        BASE_DIR = Path(__file__).parent.parent
        sql_dir = BASE_DIR / "sql"
        with open(sql_dir / "view.sql") as f:
            conn.execute(text(f.read()))
        with open(sql_dir / "trigger.sql") as f:
            conn.execute(text(f.read()))

    #Open session
    Session = sessionmaker(bind=engine)
    session = Session()

    with Session() as session:
        # RoomA = Room(room_name="Room A")
        # RoomB = Room(room_name="Room B")
        # RoomC = Room(room_name="Room C")
        # session.add_all([RoomA, RoomB, RoomC])
        # session.commit()

        # Run your terminal UI, passing the session
        prepopulate_all(session)
        terminal_UI.main_menu(session)

    session.close()

def prepopulate_all(session):
    # ----------------------
    # Members
    # ----------------------
    m1 = Member(name="Alice Johnson", date_of_birth=date(1990, 5, 12),
                gender="F", contact_detail="alice@example.com")
    m2 = Member(name="Bob Smith", date_of_birth=date(1985, 9, 23),
                gender="M", contact_detail="bob@example.com")
    session.add_all([m1, m2])
    session.flush()

    # ----------------------
    # Health Metrics
    # ----------------------
    hm1 = HealthMetric(member_id=m1.member_id, date_recorded=date.today(),
                       weight=60.5, height=165.2, heart_rate=72)
    hm2 = HealthMetric(member_id=m2.member_id, date_recorded=date.today(),
                       weight=82.3, height=178.4, heart_rate=80)
    session.add_all([hm1, hm2])

    # ----------------------
    # Billing
    # ----------------------
    bill1 = BillingPayment(member_id=m1.member_id, type_of_billing="Membership",
                           amount_due=49.99, status="Paid", payment_method="Credit Card")
    bill2 = BillingPayment(member_id=m2.member_id, type_of_billing="Membership",
                           amount_due=49.99, status="Pending", payment_method=None)
    session.add_all([bill1, bill2])

    # ----------------------
    # Goal Types & Health Goals
    # ----------------------
    gt1 = GoalType(description="Lose Weight", target="5kg in 2 months")
    gt2 = GoalType(description="Gain Muscle", target="Upper body strength")
    session.add_all([gt1, gt2])
    session.flush()

    hg1 = HealthGoal(member_id=m1.member_id, goal_type_id=gt1.goal_type_id)
    hg2 = HealthGoal(member_id=m2.member_id, goal_type_id=gt2.goal_type_id)
    session.add_all([hg1, hg2])

    # ----------------------
    # Admins
    # ----------------------
    admin1 = Admin(name="Manager1")
    session.add(admin1)
    session.flush()

    # ----------------------
    # Equipment Management
    # ----------------------
    eq1 = EquipmentManagement(admin_id=admin1.admin_id,
                              admin_operation="Treadmill maintenance",
                              status="Completed")
    eq2 = EquipmentManagement(admin_id=admin1.admin_id,
                              admin_operation="Bike repair",
                              status="Pending")
    session.add_all([eq1, eq2])

    # ----------------------
    # Rooms
    # ----------------------
    r1 = Room(room_name="Studio A")
    r2 = Room(room_name="Studio B")
    session.add_all([r1, r2])
    session.flush()

    # ----------------------
    # Room Bookings
    # ----------------------
    now = datetime.now()
    rb1 = RoomBooking(admin_id=admin1.admin_id, room_id=r1.room_id,
                      is_booked=True,
                      start_time=now + timedelta(hours=1),
                      end_time=now + timedelta(hours=2))
    rb2 = RoomBooking(admin_id=admin1.admin_id, room_id=r2.room_id,
                      is_booked=True,
                      start_time=now + timedelta(hours=3),
                      end_time=now + timedelta(hours=4))
    session.add_all([rb1, rb2])
    session.flush()

    # ----------------------
    # Trainers
    # ----------------------
    t1 = Trainer(name="Sarah Trainer")
    t2 = Trainer(name="John Coach")
    session.add_all([t1, t2])
    session.flush()

    # ----------------------
    # Fitness Classes
    # ----------------------
    fc1 = FitnessClass(trainer_id=t1.trainer_id, booking_id=rb1.booking_id,
                       class_name="Yoga Basics", capacity=20, num_signed_up=5)
    fc2 = FitnessClass(trainer_id=t2.trainer_id, booking_id=rb2.booking_id,
                       class_name="HIIT Blast", capacity=15, num_signed_up=8)
    session.add_all([fc1, fc2])
    session.flush()

    # ----------------------
    # Group Members
    # ----------------------
    gm1 = GroupMember(class_id=fc1.class_id, member_id=m1.member_id)
    gm2 = GroupMember(class_id=fc2.class_id, member_id=m2.member_id)
    session.add_all([gm1, gm2])

    # ----------------------
    # Trainer Availability
    # ----------------------
    avail1 = Availability(trainer_id=t1.trainer_id, is_recurring=True,
                          start_time=now + timedelta(days=1),
                          end_time=now + timedelta(days=1, hours=2))
    avail2 = Availability(trainer_id=t2.trainer_id, is_recurring=False,
                          start_time=now + timedelta(days=2),
                          end_time=now + timedelta(days=2, hours=1))
    session.add_all([avail1, avail2])
    session.flush()

    # ----------------------
    # Training Sessions
    # ----------------------
    ts1 = TrainingSession(trainer_id=t1.trainer_id,
                          booking_id=rb1.booking_id,
                          member_id=m1.member_id)
    ts2 = TrainingSession(trainer_id=t2.trainer_id,
                          booking_id=rb2.booking_id,
                          member_id=m2.member_id)
    session.add_all([ts1, ts2])

    session.commit()

main()