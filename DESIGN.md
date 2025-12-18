---

## 5. Database Design

The database uses SQLite and stores data in relational tables.

Main entities include:
- **Users** – stores login credentials
- **Transactions** – stores income, expenses, loans, and timestamps
- **Budgets** – stores budget limits per category

Each transaction belongs to one user and contains:
- Amount
- Type (Income, Expense, Loan Given, Loan Received)
- Subcategory
- Timestamp

---

## 6. User Interface Design

The user interface follows a **dashboard layout**:
- Fixed sidebar for navigation
- Main content area for charts and forms
- Cards used for grouping information
- Desktop-oriented layout

Charts are displayed using Chart.js:
- Bar chart for income vs expense
- Pie chart for expenses by category
- Line chart for balance over time

---

## 7. Security Considerations

Basic security measures are applied:
- User authentication with login and registration
- Separation of users’ data
- Server-side validation of form inputs

---

## 8. Software Development Life Cycle (SDLC)

The project follows a simplified SDLC:

1. **Requirements Analysis**  
   Identify core features: transactions, budgets, charts, filtering

2. **Design**  
   Define architecture, database schema, and UI layout

3. **Implementation**  
   Develop backend with FastAPI and frontend with HTML/CSS

4. **Testing**  
   Manual functional testing (documented in TESTING.md)

   Balance-Service/
│
├── main.py              # FastAPI application entry point
├── categories.py        # Predefined transaction categories
├── templates/           # HTML templates
│   ├── home.html
│   ├── transactions.html
│   ├── budget.html
│   ├── login.html
│   └── register.html
│
├── static/              # CSS styles
│   └── style.css
│
├── database.db          # SQLite database
├── requirements.txt     # Project dependencies
├── README.md            # Project description
├── DESIGN.md            # System design documentation
└── TESTING.md           # Testing documentation

5. **Deployment**  
   Local deployment using Uvicorn server

---

## 9. Design Decisions

- SQLite was chosen for simplicity and ease of setup
- FastAPI provides fast development and clear routing
- Chart.js allows lightweight and interactive data visualization
- Desktop-focused UI matches course requirements

---

## 10. Limitations and Future Improvements

Current limitations:
- No automated tests
- Local deployment only
- Basic authentication

Possible future improvements:
- Automated testing
- User roles
- Cloud deployment
- API documentation

---

## 11. Conclusion

The system design meets the project requirements and provides a stable, understandable, and maintainable solution suitable for an academic environment.