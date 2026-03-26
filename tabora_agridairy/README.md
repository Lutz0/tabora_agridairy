# Tabora AgriDairy Management System

A web-based dairy farm management system that helps farmers manage cows, milk production, farm inventory, payments, and reporting. The system improves farm efficiency by digitizing farm records and providing analytics for milk production.

**Final Year Project** — Built with Flask (MVC), Bootstrap 5, and MySQL.

---

## Features

- **User Authentication** — Registration, login, logout. Role-based access (Admin, Farmer).
- **Cow Management** — Add, view, edit, delete cows (tag number, breed, age, health status).
- **Milk Production Tracking** — Record daily milk per cow, view history, total milk per cow.
- **Inventory Management** — Track feed, medicine, equipment; add/update quantity.
- **Payment Management** — Record and manage farmer payments (admin); farmers view own payments.
- **Reports & Analytics** — Daily/monthly milk charts, inventory by category, payments by month (Chart.js).

---

## Technology Stack

| Layer      | Technology   |
|-----------|---------------|
| Backend   | Python Flask  |
| Frontend  | HTML, CSS, JavaScript |
| UI        | Bootstrap 5   |
| Database  | MySQL         |
| ORM       | SQLAlchemy    |
| Auth      | Flask-Login   |
| Charts    | Chart.js      |

---

## Project Structure (MVC)

```
tabora_agridairy/
├── app.py                 # Flask app entry point
├── config.py              # Configuration (DB, secret key)
├── requirements.txt
├── README.md
├── database/
│   └── db.py              # SQLAlchemy instance
├── models/                # Model layer
│   ├── user.py
│   ├── cow.py
│   ├── milk.py
│   ├── inventory.py
│   └── payment.py
├── routes/                # Controller layer
│   ├── auth_routes.py
│   ├── dashboard_routes.py
│   ├── cow_routes.py
│   ├── milk_routes.py
│   ├── inventory_routes.py
│   ├── payment_routes.py
│   └── report_routes.py
├── templates/             # View layer
│   ├── layout.html
│   ├── login.html, register.html
│   ├── dashboard.html
│   ├── cows.html, cow_form.html
│   ├── milk.html, milk_form.html, milk_per_cow.html
│   ├── inventory.html, inventory_form.html
│   ├── payments.html, payment_form.html
│   └── reports.html
└── static/
    ├── css/style.css
    ├── js/dashboard.js
    └── images/
```

---

## Installation

### Prerequisites

- Python 3.10 or higher
- MySQL server (e.g. XAMPP, WAMP, or standalone MySQL)
- pip

### Steps

1. **Clone or copy the project** into a folder (e.g. `tabora_agridairy`).

2. **Create a virtual environment (recommended):**
   ```bash
   cd tabora_agridairy
   python -m venv venv
   ```
   - Windows: `venv\Scripts\activate`
   - Linux/macOS: `source venv/bin/activate`

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create MySQL database:**
   - Open MySQL (e.g. phpMyAdmin or command line).
   - Create a database: `CREATE DATABASE tabora_agridairy;`
   - Note your MySQL username and password.

5. **Configure the application:**
   - Edit `config.py` and set `SQLALCHEMY_DATABASE_URI` to your MySQL connection:
     ```text
     mysql+pymysql://USERNAME:PASSWORD@localhost:3306/tabora_agridairy
     ```
   - Optionally set environment variables:
     - `SECRET_KEY` — for session security
     - `DATABASE_URL` — same URI as above
     - `FLASK_DEBUG` — `True` or `False`

6. **Run the application:**
   ```bash
   python app.py
   ```
   The app will create tables on first run and be available at: **http://127.0.0.1:5000**

7. **First use:**
   - Register a new user (default role: farmer).
   - To test admin features, set a user’s role to `admin` in the database:
     ```sql
     UPDATE users SET role = 'admin' WHERE username = 'your_username';
     ```

---

## Running Locally

```bash
cd tabora_agridairy
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
# Configure config.py (database URI)
python app.py
```

Then open **http://127.0.0.1:5000** in your browser. Log in or register to use the system.

---

## Default Configuration

- **Host:** `0.0.0.0` (all interfaces)
- **Port:** `5000`
- **Debug:** From `FLASK_DEBUG` or `True` in `config.py`

---

## License & Attribution

This project is for educational purposes (Final Year Project). Use and modify as needed for your coursework.
