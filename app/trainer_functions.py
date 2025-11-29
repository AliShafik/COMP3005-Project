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
def view_availability(session: Session, trainer_id: int):
    availabilities = session.query(Availability).filter(Availability.trainer_id == trainer_id).all()
    for availability in availabilities:
        print(availability)

#Add availability for trainer
def set_availability(session: Session, trainer_id: int, start_time: str, end_time: str, is_recurring: bool):
    start_time = datetime.fromisoformat(start_time)
    end_time = datetime.fromisoformat(end_time)

    # Query for any overlapping availability
    conflict = session.query(Availability).filter(Availability.trainer_id == trainer_id, Availability.start_time < end_time, Availability.end_time > start_time).first()
    if conflict:
        print("Error: This availability conflicts with an existing time block:")
        print(f"Existing: {conflict.start_time} → {conflict.end_time}")
        return

    availability = Availability(trainer_id=trainer_id, start_time=start_time, end_time=end_time, is_recurring=is_recurring)
    session.add(availability)
    session.commit()
    print("Availability set.")

#View schedule for trainer
def schedule_view(session: Session, trainer_id: int):
    all_training_sessions = session.query(TrainingSession).filter(TrainingSession.trainer_id == trainer_id).all()
    all_fitness_classes = session.query(FitnessClass).filter(FitnessClass.trainer_id == trainer_id).all()

    #Print results
    for sessions in all_training_sessions:
        print(sessions)
    for classes in all_fitness_classes:
        print(classes)
    
#Show goal and latest health metric for member
def member_lookup(session: Session, member_name: str):
    member_id = session.query(Member).filter(Member.name == member_name).first().member_id

    #Get goals
    goal_id = session.query(HealthGoal).filter(HealthGoal.member_id == member_id).all()
    for id in goal_id:
        goal_type = session.query(GoalType).filter(GoalType.goal_type_id == id.goal_type_id).first()
        print("Goal: ", goal_type)

    #Get latest health metric
    health_metric = session.query(HealthMetric).filter(HealthMetric.member_id == member_id).order_by(HealthMetric.date_recorded.desc()).first()
    print("Latest Health Metric: ", health_metric)