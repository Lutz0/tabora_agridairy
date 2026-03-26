"""
Tabora AgriDairy - Settings Model
Stores configurable farm settings.
"""
from database.db import db


class Setting(db.Model):
    """Simple key-value settings table."""
    __tablename__ = 'settings'

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(80), unique=True, nullable=False)
    value = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Setting {self.key}>'

