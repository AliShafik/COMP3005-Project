from sqlalchemy.orm import Session
import sys, os
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.schemas import Availability, TrainingSession, FitnessClass, Member, HealthGoal, GoalType, HealthMetric

#Add availability for trainer
def set_availability(session: Session, trainer_id: int, start_time: str, end_time: str, is_recurring: bool):
    start_time = datetime.fromisoformat(start_time)
    end_time = datetime.fromisoformat(end_time)
    availability = Availability(trainer_id=trainer_id, start_time=start_time, end_time=end_time, is_recurring=is_recurring)
    session.add(availability)
    session.commit()

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
        goal = session.query(GoalType).filter(GoalType.goal_type_id == id).first()
        print("Current Goal: " + goal)

    #Get latest health metric
    health_metric = session.query(HealthMetric).filter(HealthMetric.member_id == member_id).order_by(HealthMetric.date_recorded.desc()).first()
    print("Latest Health Metric: " + health_metric)