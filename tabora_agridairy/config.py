"""
Tabora AgriDairy - Configuration
Database URI, secret key, and debug settings.
"""
import os
from urllib.parse import quote_plus

# Base directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Application configuration."""
    ENV = os.environ.get('FLASK_ENV', 'production').lower()

    # Secret key for session management (set via env in production)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-only-secret-key-change-me'

    # MySQL Database URI
    # Format: mysql+pymysql://username:password@host:port/database_name
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or (
        f"mysql+pymysql://{os.environ.get('DB_USER', 'root')}:"
        f"{quote_plus(os.environ.get('DB_PASSWORD', ''))}@"
        f"{os.environ.get('DB_HOST', 'localhost')}:"
        f"{os.environ.get('DB_PORT', '3306')}/"
        f"{os.environ.get('DB_NAME', 'tabora_agridairy')}"
    )

    # Disable track modifications to avoid overhead
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Debug mode (off by default; set FLASK_DEBUG=true for local dev)
    DEBUG = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
