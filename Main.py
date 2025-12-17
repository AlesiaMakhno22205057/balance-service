from fastapi import FastAPI, Request, Form, Depends, HTTPException, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from starlette.status import HTTP_302_FOUND

from sqlalchemy.orm import Session
from sqlalchemy import func

from datetime import datetime
from typing import Optional
from collections import defaultdict
import logging

from database import SessionLocal
from models_db import User, Balance, Transaction as DBTransaction, Budget
from categories import CATEGORIES

# =====================================================
# LOGGING
# =====================================================
logging.basicConfig(
    filename="balance_service.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# =====================================================
# APP SETUP
# =====================================================
app = FastAPI(title="User Balance Service", version="1.0")

app.add_middleware(SessionMiddleware, secret_key="supersecretkey")

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# =====================================================
# DB DEPENDENCY
# =====================================================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# =====================================================
# AUTH
# =====================================================
@app.get("/", response_class=HTMLResponse)
def landing_page(request: Request):
    return templates.TemplateResponse("auth.html", {"request": request})


@app.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.username == username).first()
    if not user or user.password != password:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Invalid username or password"},
        )

    request.session["user_id"] = user.id
    request.session["username"] = user.username
    return RedirectResponse("/home", status_code=HTTP_302_FOUND)


@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=HTTP_302_FOUND)


@app.get("/register", response_class=HTMLResponse)
def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/register")
def register(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    initial_balance: float = Form(...),
    db: Session = Depends(get_db),
):
    if db.query(User).filter(User.username == username).first():
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "error": "Username already exists"},
        )

    user = User(username=username, password=password)
    db.add(user)
    db.flush()

    db.add(Balance(user_id=user.id, amount=initial_balance))
    db.commit()

    return RedirectResponse("/", status_code=HTTP_302_FOUND)

# =====================================================
# HOME (FIXED BALANCE OVER TIME)
# =====================================================
@app.get("/home", response_class=HTMLResponse)
def home(
    request: Request,
    db: Session = Depends(get_db),
):
    user_id = request.session.get("user_id")
    username = request.session.get("username")

    if not user_id:
        return RedirectResponse("/", status_code=HTTP_302_FOUND)

    balance_row = db.query(Balance).filter_by(user_id=user_id).first()
    current_balance = balance_row.amount if balance_row else 0

    transactions = (
        db.query(DBTransaction)
        .filter(DBTransaction.user_id == user_id)
        .order_by(DBTransaction.timestamp.asc())
        .all()
    )

    # ------------------------------
    # 📊 CHART DATA
    # ------------------------------
    income_expense_by_month = defaultdict(lambda: {"Income": 0, "Expense": 0})
    subcategory_totals = defaultdict(float)
    balance_over_time = []

    running_balance = 0

    for tx in transactions:
        month = tx.timestamp.strftime("%Y-%m")

        # Income vs Expense
        if tx.type in ["Income", "Expense"]:
            income_expense_by_month[month][tx.type] += tx.amount

        # Expenses by category
        if tx.type == "Expense":
            subcategory_totals[tx.subcategory] += tx.amount

        # Balance over time (PER TRANSACTION)
        if tx.type in ["Income", "Loan Received"]:
            running_balance += tx.amount
        else:
            running_balance -= tx.amount

        balance_over_time.append({
            "date": tx.timestamp.strftime("%Y-%m-%d %H:%M"),
            "balance": running_balance,
        })

    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "username": username,
            "balance": current_balance,
            "income_expense_by_month": dict(income_expense_by_month),
            "subcategory_totals": dict(subcategory_totals),
            "balance_over_time": balance_over_time,
        },
    )

# =====================================================
# TRANSACTIONS
# =====================================================
@app.post("/transaction")
def create_transaction(
    request: Request,
    amount: float = Form(...),
    type: str = Form(...),
    subcategory: str = Form(...),
    db: Session = Depends(get_db),
):
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse("/", status_code=HTTP_302_FOUND)

    balance = db.query(Balance).filter_by(user_id=user_id).first()
    if not balance:
        balance = Balance(user_id=user_id, amount=0)
        db.add(balance)
        db.flush()

    if type in ["Income", "Loan Received"]:
        balance.amount += amount
    else:
        balance.amount -= amount

    db.add(
        DBTransaction(
            user_id=user_id,
            amount=amount,
            type=type,
            subcategory=subcategory,
            timestamp=datetime.utcnow(),
            service_id=0,
            order_id=0,
        )
    )

    db.commit()
    return RedirectResponse("/transactions", status_code=HTTP_302_FOUND)


@app.get("/transactions", response_class=HTMLResponse)
def transactions_page(
    request: Request,
    db: Session = Depends(get_db),
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    min_amount: Optional[float] = None,
    max_amount: Optional[float] = None,
    tx_type: Optional[str] = None,
    category: Optional[str] = None,
):
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse("/", status_code=HTTP_302_FOUND)

    query = db.query(DBTransaction).filter(DBTransaction.user_id == user_id)

    if start_date:
        query = query.filter(DBTransaction.timestamp >= datetime.fromisoformat(start_date))
    if end_date:
        query = query.filter(DBTransaction.timestamp <= datetime.fromisoformat(end_date))
    if min_amount is not None:
        query = query.filter(DBTransaction.amount >= min_amount)
    if max_amount is not None:
        query = query.filter(DBTransaction.amount <= max_amount)
    if tx_type and tx_type != "All":
        query = query.filter(DBTransaction.type == tx_type)
    if category:
        query = query.filter(DBTransaction.subcategory == category)

    transactions = query.order_by(DBTransaction.timestamp.desc()).all()

    return templates.TemplateResponse(
        "transactions.html",
        {
            "request": request,
            "transactions": transactions,
            "categories": CATEGORIES,
            "filters": {
                "start_date": start_date,
                "end_date": end_date,
                "min_amount": min_amount,
                "max_amount": max_amount,
                "tx_type": tx_type or "All",
                "category": category or "",
            },
        },
    )

# =====================================================
# BUDGET
# =====================================================
@app.get("/budget", response_class=HTMLResponse)
def budget_page(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse("/", status_code=HTTP_302_FOUND)

    budgets = db.query(Budget).filter(Budget.user_id == user_id).all()

    expenses = (
        db.query(DBTransaction.subcategory, func.sum(DBTransaction.amount))
        .filter(DBTransaction.user_id == user_id, DBTransaction.type == "Expense")
        .group_by(DBTransaction.subcategory)
        .all()
    )

    expenses_dict = {c: float(a or 0) for c, a in expenses}

    budget_data = []
    for b in budgets:
        spent = expenses_dict.get(b.category, 0)
        percent = (spent / b.amount) * 100 if b.amount else 0
        status = "ok" if percent < 80 else "warning" if percent <= 100 else "danger"

        budget_data.append({
            "id": b.id,
            "category": b.category,
            "budget": b.amount,
            "spent": spent,
            "percent": round(percent, 1),
            "status": status,
        })

    return templates.TemplateResponse(
        "budget.html",
        {
            "request": request,
            "categories": CATEGORIES,
            "budget_data": budget_data,
        },
    )


@app.post("/budget")
def add_budget(
    request: Request,
    category: str = Form(...),
    amount: float = Form(...),
    db: Session = Depends(get_db),
):
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse("/", status_code=HTTP_302_FOUND)

    budget = db.query(Budget).filter_by(user_id=user_id, category=category).first()
    if budget:
        budget.amount = amount
    else:
        db.add(Budget(user_id=user_id, category=category, amount=amount))

    db.commit()
    return RedirectResponse("/budget", status_code=HTTP_302_FOUND)


@app.post("/budget/delete")
def delete_budget(
    request: Request,
    budget_id: int = Form(...),
    db: Session = Depends(get_db),
):
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse("/", status_code=HTTP_302_FOUND)

    budget = db.query(Budget).filter_by(id=budget_id, user_id=user_id).first()
    if budget:
        db.delete(budget)
        db.commit()

    return RedirectResponse("/budget", status_code=HTTP_302_FOUND)