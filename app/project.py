from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
import datetime
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.base import Base, Member

#Connect to db (change to your own local db)
engine = create_engine("postgresql://test:test@localhost:5432/project")

#Create tables
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

#Open session
Session = sessionmaker(bind=engine)
session = Session()

#Add to tables
m1 = Member(name="Danial", date_of_birth=datetime.date(2004, 4, 22), gender="Male", contact_detail="danialmcintyre@cmail.carleton.ca")
session.add_all([m1])
session.commit()

all_members = session.query(Member).all()
print(all_members)

session.close()