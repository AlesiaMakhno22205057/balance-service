import pytest
from fastapi.testclient import TestClient
from main import app
from models_db import User, Transaction
from database import Base, engine, SessionLocal
from datetime import datetime

client = TestClient(app)