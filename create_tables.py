# create_tables.py
from database import Base, engine
from models_db import User, Balance, Reservation, Transaction

Base.metadata.create_all(bind=engine)
print("Tables created successfully")
