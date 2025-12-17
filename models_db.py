from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

# ======================
# USER
# ======================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(100), nullable=False)

    balances = relationship("Balance", back_populates="user", cascade="all, delete")
    reservations = relationship("Reservation", back_populates="user", cascade="all, delete")
    transactions = relationship("Transaction", back_populates="user", cascade="all, delete")
    budgets = relationship("Budget", back_populates="user", cascade="all, delete")

# ======================
# BALANCE
# ======================
class Balance(Base):
    __tablename__ = "balances"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float, default=0.0)

    user = relationship("User", back_populates="balances")

# ======================
# RESERVATION
# ======================
class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    service_id = Column(Integer, nullable=False)
    order_id = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(String(50), default="reserved")

    user = relationship("User", back_populates="reservations")

# ======================
# TRANSACTION
# ======================
class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    service_id = Column(Integer, nullable=False)
    order_id = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    type = Column(String(50), default="deposit")
    subcategory = Column(String(100), default="Other")

    user = relationship("User", back_populates="transactions")

# ======================
# BUDGET  
# ======================
class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)  
    user_id = Column(Integer, ForeignKey("users.id"))
    category = Column(String(100), nullable=False)
    amount = Column(Float, nullable=False)

    user = relationship("User", back_populates="budgets")