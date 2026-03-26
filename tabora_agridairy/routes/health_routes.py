"""
Tabora AgriDairy - Health Tracking Routes
Add and list health records for cows.
"""
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from database.db import db
from models.cow import Cow
from models.health_record import HealthRecord


health_bp = Blueprint('health', __name__)


def get_cows_queryset():
    if current_user.is_admin():
        return Cow.query
    return Cow.query.filter_by(owner_id=current_user.id)


@health_bp.route('/health_records')
@login_required
def list_health_records():
    """List health records."""
    if current_user.is_admin():
        records = HealthRecord.query.order_by(HealthRecord.date.desc(), HealthRecord.id.desc()).all()
    else:
        cow_ids = [c.id for c in get_cows_queryset().all()]
        records = HealthRecord.query.filter(HealthRecord.cow_id.in_(cow_ids)).order_by(
            HealthRecord.date.desc(), HealthRecord.id.desc()
        ).all() if cow_ids else []
    return render_template('health_records.html', records=records)


@health_bp.route('/add_health_record', methods=['GET', 'POST'])
@login_required
def add_health_record():
    """Add a cow health record."""
    cows = get_cows_queryset().order_by(Cow.tag_number).all()
    if request.method == 'POST':
        cow_id = request.form.get('cow_id', type=int)
        disease = request.form.get('disease', '').strip()
        treatment = request.form.get('treatment', '').strip()
        date_str = request.form.get('date', '').strip()

        if not cow_id or not disease or not treatment or not date_str:
            flash('Cow, disease, treatment, and date are required.', 'danger')
            return render_template('add_health_record.html', cows=cows), 400

        cow = Cow.query.get(cow_id)
        if not cow or (not current_user.is_admin() and cow.owner_id != current_user.id):
            flash('Invalid cow selection.', 'danger')
            return render_template('add_health_record.html', cows=cows), 403

        try:
            record_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid date format.', 'danger')
            return render_template('add_health_record.html', cows=cows), 400

        record = HealthRecord(
            cow_id=cow_id,
            disease=disease,
            treatment=treatment,
            date=record_date
        )
        db.session.add(record)
        db.session.commit()
        flash('Health record added successfully.', 'success')
        return redirect(url_for('health.list_health_records'))

    return render_template('add_health_record.html', cows=cows)

