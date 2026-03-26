"""
Tabora AgriDairy - Milk Production Model
Tracks daily milk production per cow.
"""
from database.db import db


class MilkProduction(db.Model):
    """Milk production record per cow per date."""
    __tablename__ = 'milk_production'

    id = db.Column(db.Integer, primary_key=True)
    cow_id = db.Column(db.Integer, db.ForeignKey('cows.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    quantity_liters = db.Column(db.Float, nullable=False)
    notes = db.Column(db.Text, nullable=True)

    # Unique constraint: one record per cow per date (optional - can have multiple entries per day)
    __table_args__ = (db.Index('idx_cow_date', 'cow_id', 'date'),)

    def __repr__(self):
        return f'<MilkProduction cow_id={self.cow_id} date={self.date} qty={self.quantity_liters}>'
