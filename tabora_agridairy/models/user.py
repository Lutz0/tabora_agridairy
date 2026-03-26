"""
Tabora AgriDairy - User Model
Stores user credentials and role for authentication.
"""
from flask_login import UserMixin
from database.db import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    """User model for authentication and role-based access."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='farmer')  # 'admin' or 'farmer'

    # Relationships
    cows = db.relationship('Cow', backref='owner', lazy='dynamic', foreign_keys='Cow.owner_id')
    payments = db.relationship('Payment', backref='farmer', lazy='dynamic', foreign_keys='Payment.farmer_id')

    def set_password(self, password):
        """Hash and set the user's password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify password against hash."""
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        """Check if user has admin role."""
        return self.role == 'admin'

    def __repr__(self):
        return f'<User {self.username}>'
