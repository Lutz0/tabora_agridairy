"""
Tabora AgriDairy - Cow Management Routes (Controller)
CRUD: Add, view, edit, delete cows.
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from database.db import db
from models.cow import Cow

cow_bp = Blueprint('cow', __name__)


def get_cows_queryset():
    """Admin: all cows; Farmer: own cows only."""
    if current_user.is_admin():
        return Cow.query
    return Cow.query.filter_by(owner_id=current_user.id)


@cow_bp.route('/')
@cow_bp.route('/cows')
@login_required
def list_cows():
    """View all cows."""
    cows = get_cows_queryset().order_by(Cow.tag_number).all()
    return render_template('cows.html', cows=cows)


@cow_bp.route('/add', methods=['GET', 'POST'])
@cow_bp.route('/add_cow', methods=['GET', 'POST'])
@login_required
def add_cow():
    """Add a new cow. Supports form POST and JSON POST."""
    if request.method == 'GET':
        return render_template('add_cow.html', cow=None)

    is_json = request.is_json
    payload = request.get_json(silent=True) if is_json else request.form

    tag_number = (payload.get('tag_number') or '').strip()
    breed = (payload.get('breed') or '').strip()
    age_raw = payload.get('age')
    status = (payload.get('status') or payload.get('health_status') or 'Healthy').strip()

    try:
        age = int(age_raw) if age_raw is not None and str(age_raw).strip() != '' else None
    except (TypeError, ValueError):
        age = None

    if not tag_number or not breed or age is None or age < 0 or not status:
        msg = 'Tag number, breed, age (>= 0), and status are required.'
        if is_json:
            return jsonify({'success': False, 'message': msg}), 400
        flash(msg, 'danger')
        return render_template('add_cow.html', cow=None), 400

    if Cow.query.filter_by(tag_number=tag_number).first():
        msg = f'Cow with tag number "{tag_number}" already exists.'
        if is_json:
            return jsonify({'success': False, 'message': msg}), 409
        flash(msg, 'danger')
        return render_template('add_cow.html', cow=None), 409

    cow = Cow(
        tag_number=tag_number,
        breed=breed,
        age=age,
        health_status=status,
        owner_id=current_user.id
    )
    db.session.add(cow)
    db.session.commit()

    if is_json:
        return jsonify({'success': True, 'message': 'Cow added successfully', 'cow_id': cow.id}), 201

    flash('Cow added successfully', 'success')
    return redirect(url_for('cow.list_cows'))


@cow_bp.route('/edit/<int:cow_id>', methods=['GET', 'POST'])
@cow_bp.route('/edit_cow/<int:cow_id>', methods=['GET', 'POST'])
@login_required
def edit_cow(cow_id):
    """Edit an existing cow."""
    cow = Cow.query.get_or_404(cow_id)
    if not current_user.is_admin() and cow.owner_id != current_user.id:
        flash('You do not have permission to edit this cow.', 'danger')
        return redirect(url_for('cow.list_cows'))

    if request.method == 'POST':
        tag_number = request.form.get('tag_number', '').strip() or cow.tag_number
        breed = request.form.get('breed', '').strip()
        age = request.form.get('age', type=int)
        status = request.form.get('status', request.form.get('health_status', 'Healthy')).strip()

        if not tag_number or not breed or age is None or age < 0 or not status:
            flash('Tag number, breed, age and status are required.', 'danger')
            return render_template('cow_form.html', cow=cow), 400

        duplicate = Cow.query.filter(Cow.tag_number == tag_number, Cow.id != cow.id).first()
        if duplicate:
            flash(f'Cow with tag number "{tag_number}" already exists.', 'danger')
            return render_template('cow_form.html', cow=cow), 409

        cow.tag_number = tag_number
        cow.breed = breed
        cow.age = age
        cow.health_status = status
        db.session.commit()
        flash('Cow updated successfully.', 'success')
        return redirect(url_for('cow.list_cows'))
    return render_template('cow_form.html', cow=cow)


@cow_bp.route('/delete/<int:cow_id>', methods=['POST'])
@cow_bp.route('/delete_cow/<int:cow_id>', methods=['POST'])
@login_required
def delete_cow(cow_id):
    """Delete a cow."""
    cow = Cow.query.get_or_404(cow_id)
    if not current_user.is_admin() and cow.owner_id != current_user.id:
        flash('You do not have permission to delete this cow.', 'danger')
        return redirect(url_for('cow.list_cows'))
    db.session.delete(cow)
    db.session.commit()
    flash('Cow deleted successfully.', 'success')
    return redirect(url_for('cow.list_cows'))
