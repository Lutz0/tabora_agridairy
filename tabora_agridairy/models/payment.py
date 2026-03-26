"""
Tabora AgriDairy - Payment Model
Tracks payments to farmers.
"""
from database.db import db


class Payment(db.Model):
    """Payment record for farmers."""
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.Date, nullable=False)
    payment_method = db.Column(db.String(20), nullable=False, default='Cash')  # Mpesa, Cash, Card
    reference = db.Column(db.String(120), nullable=True)
    description = db.Column(db.Text, nullable=True)

    @property
    def date(self):
        """Alias used by forms requiring 'date'."""
        return self.payment_date

    @date.setter
    def date(self, value):
        self.payment_date = value

    def __repr__(self):
        return f'<Payment farmer_id={self.farmer_id} amount={self.amount}>'
