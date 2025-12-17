# seed_db.py

from sqlalchemy.orm import Session
from database import SessionLocal
from models_db import User, Balance

db: Session = SessionLocal()

# Simple, easy-to-test user IDs
users = [
    {"id": 1, "username": "alice", "balance": 100.0},
    {"id": 2, "username": "bob", "balance": 50.0},
    {"id": 3, "username": "charlie", "balance": 75.5},
]

for u in users:
    user = User(id=u["id"], username=u["username"])
    db.add(user)
    db.flush()  # makes sure user.id is available before using it

    balance = Balance(user_id=user.id, amount=u["balance"])
    db.add(balance)

db.commit()
print("✅ Users added: 1, 2, 3")