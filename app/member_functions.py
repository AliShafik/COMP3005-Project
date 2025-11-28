from sqlalchemy.orm import Session
from sqlalchemy import Numeric
import sys, os
from datetime import date

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.schemas import Member, GoalType, HealthMetric, HealthGoal

def register_user(session: Session, name: str, date_of_birth: date, gender: str, contact_detail: str):
    existing_member = session.query(Member).filter_by(contact_detail=contact_detail).first()
    if existing_member:
        print("Error: contact details must be unique!")
    else:
        user = Member(name=name, date_of_birth=date_of_birth, gender=gender, contact_detail=contact_detail)
        session.add(user)
        session.commit()
        print(f"{name} has successfully been registered.")

def login_user(session: Session, name: str):
    member = session.query(Member).filter(Member.name == name).first()
    if member:
        print(f"Welcome back, {member.name}!")
        return member.member_id
    else:
        print("Member not found. Please register first.")
        return None

def update_personal_details(session: Session, id: int, name="null", date_of_birth = "null", gender = "null", contact = "null"):
    name = ""
    member = session.query(Member).filter(Member.member_id == id).first()
    if(name != "null"):
        member.name = name
    if(date_of_birth != "null"):
        member.date_of_birth = date_of_birth
    if(gender != "null"):
        member.gender = gender
    if(contact != "null"):
        member.contact_detail = contact
    return


def show_fitness_goals(session: Session, member_id: int):
    goals = session.query(HealthGoal).filter(HealthGoal.member_id == member_id).all()
    for i, goal in enumerate(goals):
        print(f"Goal {i + 1}: {goal}")

def update_fitness_goals(session: Session, user_index: int, member_id:int, goal_id: int, target: str):
    goal = session.query(HealthGoal).filter(HealthGoal.member_id == member_id).all()[user_index - 1]
    goal_type = session.query(GoalType).filter(GoalType.goal_type_id == goal.goal_type_id).first() 
    goal_type.target = target
    session.commit()
    
def input_health_metric(session: Session, member_id: int, date_recorded: date, weight: float, height: float, heart_rate: int):
    healthMetric = HealthMetric(member_id, date_recorded, weight, height, heart_rate)
    session.add(healthMetric)
    session.commit()

def dashboard(): return
def PT_session_scheduling(): return
def class_registrtion(): return
"""
User Registration: Create a new member with unique email and basic profile info.
● Profile Management: Update personal details, fitness goals (e.g., weight target), and input new
health metrics (e.g., weight, heart rate).
● Health History: Log multiple metric entries; do not overwrite. Must support time-stamped
entries.
● Dashboard: Show latest health stats, active goals, past class count, upcoming sessions.
● PT Session Scheduling: Book or reschedule training with a trainer, validating availability and
room conflicts.
● Group Class Registration: Register for scheduled classes if capacity permits.
"""