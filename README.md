# Personal Finance Dashboard

A desktop-style financial management application built as part of a university course.
The project allows users to track income and expenses, manage budgets, and visualize financial data.

## Features
- User registration and login
- Add / edit / delete transactions
- Income & expense tracking
- Budget planner with progress bars
- Charts (income vs expense, expenses by category, balance over time)
- Transaction filtering by date, amount, type, and category

## Tech Stack
- Python
- FastAPI
- HTML / CSS
- Chart.js
- SQLite

## Project Structure
- `main.py` – FastAPI application entry point
- `templates/` – HTML templates
- `static/` – CSS styles
- `database.db` – SQLite database
- `requirements.txt` – Python dependencies

## How to Run

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload

Open your browser and go to:
http://127.0.0.1:8000