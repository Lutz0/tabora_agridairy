"""
Tabora AgriDairy - Milk Production Routes (Controller)
Record daily milk, view records, total milk per cow, history.
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from database.db import db
from models.cow import Cow
from models.milk import MilkProduction
from sqlalchemy import func
from datetime import date, datetime

milk_bp = Blueprint('milk', __name__)


def get_cows_queryset():
    if current_user.is_admin():
        return Cow.query
    return Cow.query.filter_by(owner_id=current_user.id)


@milk_bp.route('/')
@login_required
def list_records():
    """View milk production records (recent first)."""
    if current_user.is_admin():
        records = MilkProduction.query.order_by(MilkProduction.date.desc(), MilkProduction.id.desc()).limit(100).all()
    else:
        cow_ids = [c.id for c in get_cows_queryset().all()]
        records = MilkProduction.query.filter(
            MilkProduction.cow_id.in_(cow_ids) if cow_ids else False
        ).order_by(MilkProduction.date.desc(), MilkProduction.id.desc()).limit(100).all() if cow_ids else []
    return render_template('milk.html', records=records)


@milk_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_record():
    """Record daily milk production."""
    cows = get_cows_queryset().order_by(Cow.tag_number).all()
    if request.method == 'POST':
        cow_id = request.form.get('cow_id', type=int)
        date_str = request.form.get('date')
        quantity = request.form.get('quantity_liters', type=float)
        notes = request.form.get('notes', '').strip()
        if not cow_id or not date_str or quantity is None:
            flash('Cow, date, and quantity are required.', 'danger')
            return render_template('milk_form.html', cows=cows, record=None)
        cow = Cow.query.get(cow_id)
        if not cow or (not current_user.is_admin() and cow.owner_id != current_user.id):
            flash('Invalid cow selected.', 'danger')
            return render_template('milk_form.html', cows=cows, record=None)
        try:
            record_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid date format.', 'danger')
            return render_template('milk_form.html', cows=cows, record=None)
        record = MilkProduction(
            cow_id=cow_id,
            date=record_date,
            quantity_liters=quantity,
            notes=notes or None
        )
        db.session.add(record)
        db.session.commit()
        flash('Milk record added successfully.', 'success')
        return redirect(url_for('milk.list_records'))
    return render_template('milk_form.html', cows=cows, record=None, default_date=date.today())


@milk_bp.route('/edit/<int:record_id>', methods=['GET', 'POST'])
@login_required
def edit_record(record_id):
    """Edit a milk production record."""
    record = MilkProduction.query.get_or_404(record_id)
    cow = Cow.query.get(record.cow_id)
    if not cow or (not current_user.is_admin() and cow.owner_id != current_user.id):
        flash('You do not have permission to edit this record.', 'danger')
        return redirect(url_for('milk.list_records'))
    cows = get_cows_queryset().order_by(Cow.tag_number).all()
    if request.method == 'POST':
        record.cow_id = request.form.get('cow_id', type=int) or record.cow_id
        date_str = request.form.get('date')
        if date_str:
            try:
                record.date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                pass
        qty = request.form.get('quantity_liters', type=float)
        if qty is not None:
            record.quantity_liters = qty
        record.notes = request.form.get('notes', '').strip() or None
        db.session.commit()
        flash('Milk record updated successfully.', 'success')
        return redirect(url_for('milk.list_records'))
    return render_template('milk_form.html', cows=cows, record=record)


@milk_bp.route('/delete/<int:record_id>', methods=['POST'])
@login_required
def delete_record(record_id):
    """Delete a milk production record."""
    record = MilkProduction.query.get_or_404(record_id)
    cow = Cow.query.get(record.cow_id)
    if not cow or (not current_user.is_admin() and cow.owner_id != current_user.id):
        flash('You do not have permission to delete this record.', 'danger')
        return redirect(url_for('milk.list_records'))
    db.session.delete(record)
    db.session.commit()
    flash('Milk record deleted successfully.', 'success')
    return redirect(url_for('milk.list_records'))


@milk_bp.route('/per-cow')
@login_required
def per_cow():
    """Total milk per cow (summary)."""
    if current_user.is_admin():
        subq = db.session.query(
            MilkProduction.cow_id,
            func.sum(MilkProduction.quantity_liters).label('total')
        ).group_by(MilkProduction.cow_id).subquery()
        results = db.session.query(Cow, subq.c.total).join(
            subq, Cow.id == subq.c.cow_id
        ).order_by(subq.c.total.desc()).all()
    else:
        cow_ids = [c.id for c in get_cows_queryset().all()]
        if not cow_ids:
            results = []
        else:
            subq = db.session.query(
                MilkProduction.cow_id,
                func.sum(MilkProduction.quantity_liters).label('total')
            ).filter(MilkProduction.cow_id.in_(cow_ids)).group_by(MilkProduction.cow_id).subquery()
            results = db.session.query(Cow, subq.c.total).join(
                subq, Cow.id == subq.c.cow_id
            ).order_by(subq.c.total.desc()).all()
    return render_template('milk_per_cow.html', results=results)
