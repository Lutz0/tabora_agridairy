"""
Tabora AgriDairy - Database Module
SQLAlchemy initialization and database connection.
"""
from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy instance - will be initialized in app.py
db = SQLAlchemy()
