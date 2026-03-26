"""
Tabora AgriDairy - Payment Routes (Controller)
Manage farmer payments: farmer, amount, date, description.
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from database.db import db
from models.user import User
from models.payment import Payment
from datetime import datetime

payment_bp = Blueprint('payment', __name__)


def get_farmers_queryset():
    """Admin: all users with role farmer; for dropdown."""
    return User.query.filter_by(role='farmer').order_by(User.username).all()


@payment_bp.route('/')
@payment_bp.route('/payments')
@login_required
def list_payments():
    """View payments (admin: all; farmer: own only)."""
    if current_user.is_admin():
        payments = Payment.query.order_by(Payment.payment_date.desc()).all()
    else:
        payments = Payment.query.filter_by(farmer_id=current_user.id).order_by(
            Payment.payment_date.desc()
        ).all()
    return render_template('payments.html', payments=payments)


@payment_bp.route('/add', methods=['GET', 'POST'])
@payment_bp.route('/add_payment', methods=['GET', 'POST'])
@login_required
def add_payment():
    """Add payment with payment method validation."""
    farmers = get_farmers_queryset()
    if request.method == 'POST':
        farmer_id = request.form.get('farmer_id', type=int) if current_user.is_admin() else current_user.id
        amount = request.form.get('amount', type=float)
        date_str = request.form.get('date') or request.form.get('payment_date')
        payment_method = request.form.get('payment_method', 'Cash').strip()
        reference = request.form.get('reference', '').strip()
        description = request.form.get('description', '').strip()
        if not farmer_id or amount is None or not date_str or not payment_method:
            flash('Farmer, amount, date, and payment method are required.', 'danger')
            return render_template('add_payment.html', payment=None, farmers=farmers)
        if payment_method not in {'Mpesa', 'Cash', 'Card'}:
            flash('Invalid payment method selected.', 'danger')
            return render_template('add_payment.html', payment=None, farmers=farmers), 400
        if payment_method == 'Mpesa' and not reference:
            flash('Mpesa reference code is required.', 'danger')
            return render_template('add_payment.html', payment=None, farmers=farmers), 400
        try:
            payment_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid date format.', 'danger')
            return render_template('add_payment.html', payment=None, farmers=farmers)
        payment = Payment(
            farmer_id=farmer_id,
            amount=amount,
            payment_date=payment_date,
            payment_method=payment_method,
            reference=reference or None,
            description=description or None
        )
        db.session.add(payment)
        db.session.commit()
        flash('Payment recorded successfully.', 'success')
        return redirect(url_for('payment.list_payments'))
    return render_template('add_payment.html', payment=None, farmers=farmers)


@payment_bp.route('/edit/<int:payment_id>', methods=['GET', 'POST'])
@login_required
def edit_payment(payment_id):
    """Edit payment (admin only)."""
    if not current_user.is_admin():
        flash('Only administrators can edit payments.', 'danger')
        return redirect(url_for('payment.list_payments'))
    payment = Payment.query.get_or_404(payment_id)
    farmers = get_farmers_queryset()
    if request.method == 'POST':
        payment.farmer_id = request.form.get('farmer_id', type=int) or payment.farmer_id
        amt = request.form.get('amount', type=float)
        if amt is not None:
            payment.amount = amt
        date_str = request.form.get('date') or request.form.get('payment_date')
        if date_str:
            try:
                payment.payment_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                pass
        payment_method = request.form.get('payment_method', payment.payment_method or 'Cash').strip()
        reference = request.form.get('reference', '').strip()
        if payment_method in {'Mpesa', 'Cash', 'Card'}:
            payment.payment_method = payment_method
        if payment.payment_method == 'Mpesa' and not reference:
            flash('Mpesa reference code is required.', 'danger')
            return render_template('payment_form.html', payment=payment, farmers=farmers), 400
        payment.reference = reference or None
        payment.description = request.form.get('description', '').strip() or None
        db.session.commit()
        flash('Payment updated successfully.', 'success')
        return redirect(url_for('payment.list_payments'))
    return render_template('payment_form.html', payment=payment, farmers=farmers)


@payment_bp.route('/delete/<int:payment_id>', methods=['POST'])
@login_required
def delete_payment(payment_id):
    """Delete payment (admin only)."""
    if not current_user.is_admin():
        flash('Only administrators can delete payments.', 'danger')
        return redirect(url_for('payment.list_payments'))
    payment = Payment.query.get_or_404(payment_id)
    db.session.delete(payment)
    db.session.commit()
    flash('Payment deleted successfully.', 'success')
    return redirect(url_for('payment.list_payments'))
