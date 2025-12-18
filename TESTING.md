# Testing

This document describes the testing process used for the Personal Finance Dashboard project.
Testing was performed manually to verify that all core features work correctly and meet the project requirements.

---

## 1. Authentication Testing

| Test Case | Description | Result |
|---------|------------|--------|
| Register user | Register with valid username and password | Passed |
| Register duplicate user | Attempt to register existing username | Passed |
| Login valid user | Login with correct credentials | Passed |
| Login invalid user | Login with incorrect password | Passed |

---

## 2. Transaction Management Testing

| Test Case | Description | Result |
|---------|------------|--------|
| Add transaction | Add income and expense transactions | Passed |
| Edit transaction | Modify amount and category | Passed |
| Delete transaction | Remove existing transaction | Passed |
| Balance update | Balance updates after add/edit/delete | Passed |

---

## 3. Budget Planner Testing

| Test Case | Description | Result |
|---------|------------|--------|
| Create budget | Set budget for a category | Passed |
| Budget progress | Progress bar updates with expenses | Passed |
| Over budget | Warning shown when limit exceeded | Passed |
| Delete budget | Remove existing budget | Passed |

---

## 4. Charts and Visualization Testing

| Test Case | Description | Result |
|---------|------------|--------|
| Income vs Expense chart | Displays monthly income and expenses | Passed |
| Expense category pie chart | Displays category distribution | Passed |
| Balance over time chart | Displays balance trend correctly | Passed |

---

## 5. Filtering Testing

| Test Case | Description | Result |
|---------|------------|--------|
| Filter by date | Transactions filtered by date range | Passed |
| Filter by amount | Transactions filtered by min/max amount | Passed |
| Filter by type | Filter income, expense, loans | Passed |
| Filter by category | Filter by transaction category | Passed |

---

## 6. Browser and UI Testing

| Test Case | Description | Result |
|---------|------------|--------|
| Layout rendering | UI displays correctly on desktop browser | Passed |
| Navigation | Sidebar links work correctly | Passed |
| Form validation | Required fields enforced | Passed |

---

## Conclusion

Manual testing confirmed that all main functionalities of the application work as expected.
The system meets the defined requirements and is ready for use as a university project.
