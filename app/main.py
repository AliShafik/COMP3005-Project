from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker
import datetime
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.schemas import Base, Member, Trainer, Admin
import terminal_UI

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
    #Base.metadata.drop_all(engine)
    Base.metadata.create_all(conn)

#Open session
Session = sessionmaker(bind=engine)
session = Session()

with Session() as session:
    # trainer1 = Trainer(name="Danial McIntyre")
    # admin1 = Admin(name="Mary Brown")
    # session.add_all([trainer1, admin1])
    # session.commit()

    # Run your terminal UI, passing the session
    terminal_UI.main_menu(session)

session.close()