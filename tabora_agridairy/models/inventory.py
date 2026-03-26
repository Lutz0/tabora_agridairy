"""
Tabora AgriDairy - Inventory Model
Tracks farm inventory (feed, medicine, equipment).
"""
from database.db import db
from datetime import datetime


class Inventory(db.Model):
    """Inventory item for farm supplies."""
    __tablename__ = 'inventory'

    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # Feed, Medicine, Equipment
    quantity = db.Column(db.Integer, nullable=False, default=0)
    unit = db.Column(db.String(30), nullable=True, default='units')  # kg, liters, pieces, etc.
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<Inventory {self.item_name} ({self.category})>'
