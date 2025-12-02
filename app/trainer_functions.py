from sqlalchemy.orm import Session
import sys, os
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.schemas import Availability, TrainingSession, FitnessClass, Member, HealthGoal, GoalType, HealthMetric, Trainer

#Register trainer
def register_trainer(session: Session, name: str):
    existing_member = session.query(Trainer).filter_by(name=name).first()
    if existing_member:
        print("Error: contact details must be unique!")
    else:
        trainer = Trainer(name=name)
        session.add(trainer)
        session.commit()
        print(f"{name} has successfully been registered as a trainer.")

#Login trainer
def login_trainer(session: Session, name: str):
    trainer = session.query(Trainer).filter(Trainer.name == name).first()
    if trainer:
        print(f"Welcome back, {trainer.name}!")
        return trainer.trainer_id
    else:
        print("Trainer not found. Please register first.")
        return None
    
def view_trainers(session: Session):
    trainers = session.query(Trainer).all()
    for trainer in trainers:
        print(trainer)

#View availability for trainer
def view_availability(session: Session, trainer: Trainer):
    if not trainer:
        print("Trainer not found")
        return

    for availability in trainer.availability:
        print(availability)

#Add availability for trainer
def set_availability(session: Session, trainer: Trainer, start_time: str, end_time: str, is_recurring: bool):
    start_time = datetime.fromisoformat(start_time)
    end_time = datetime.fromisoformat(end_time)

    if not trainer:
        print("Trainer not found")
        return
    
    for availability in trainer.availability:
        if start_time < availability.end_time and end_time > availability.start_time:
            print("Error: Conflict with:", availability)
            return
        
    availability = Availability(trainer=trainer, start_time=start_time, end_time=end_time, is_recurring=is_recurring)
    session.add(availability)
    session.commit()
    print("Availability set.")

#View schedule for trainer
def schedule_view(session: Session, trainer: Trainer):
    if not trainer:
        print("Trainer not found")
        return

    # All training sessions
    for training_session in trainer.sessions:
        print(training_session)

    # All fitness classes
    for fitness_class in trainer.classes:
        print(fitness_class)
    
#Show goal and latest health metric for member
def member_lookup(session: Session, member_name: str):
    member = session.query(Member).filter(Member.name == member_name).first()
    if not member:
        print("Member not found")
        return
    
    #Get goals
    for goal in member.goals:
        print("Goal:", goal.goal_type)

    #Get health metrics
    latest_metric = max(member.health_metrics, key=lambda m: m.date_recorded, default=None)
    print("Latest Health Metric:", latest_metric)