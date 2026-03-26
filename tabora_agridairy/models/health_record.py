"""
Tabora AgriDairy - Health Record Model
Tracks disease/treatment history for cows.
"""
from database.db import db


class HealthRecord(db.Model):
    """Health records linked to cows."""
    __tablename__ = 'health_records'

    id = db.Column(db.Integer, primary_key=True)
    cow_id = db.Column(db.Integer, db.ForeignKey('cows.id'), nullable=False, index=True)
    disease = db.Column(db.String(150), nullable=False)
    treatment = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date, nullable=False)

    cow = db.relationship('Cow', backref=db.backref('health_records', lazy='dynamic', cascade='all, delete-orphan'))

    def __repr__(self):
        return f'<HealthRecord cow_id={self.cow_id} disease={self.disease}>'

