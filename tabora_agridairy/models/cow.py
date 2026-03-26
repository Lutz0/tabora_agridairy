"""
Tabora AgriDairy - Cow Model
Stores cow information and links to owner.
"""
from database.db import db


class Cow(db.Model):
    """Cow model for livestock management."""
    __tablename__ = 'cows'

    id = db.Column(db.Integer, primary_key=True)
    tag_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    breed = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)  # Age in years
    health_status = db.Column(db.String(50), nullable=False, default='Healthy')  # e.g. Healthy, Sick, Under Treatment
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relationship to milk production records
    milk_records = db.relationship('MilkProduction', backref='cow', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Cow {self.tag_number}>'
