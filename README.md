# Personal Finance Dashboard

A desktop-style financial management application built for a university course.

## Features
- User registration and login
- Add / edit / delete transactions
- Income & expense tracking
- Budget planner with progress bars
- Charts (bar, pie, balance over time)
- Transaction filtering

## Tech Stack
- Python
- FastAPI
- HTML / CSS
- Chart.js
- SQLite

## How to Run

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload