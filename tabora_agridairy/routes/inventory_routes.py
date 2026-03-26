"""
Tabora AgriDairy - Inventory Routes (Controller)
Add item, update quantity, view list (Feed, Medicine, Equipment).
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from database.db import db
from models.inventory import Inventory

inventory_bp = Blueprint('inventory', __name__)


@inventory_bp.route('/')
@login_required
def list_items():
    """View all inventory items."""
    items = Inventory.query.order_by(Inventory.category, Inventory.item_name).all()
    return render_template('inventory.html', items=items)


@inventory_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_item():
    """Add new inventory item."""
    if request.method == 'POST':
        item_name = request.form.get('item_name', '').strip()
        category = request.form.get('category', 'Feed').strip()
        quantity = request.form.get('quantity', type=int)
        unit = request.form.get('unit', 'units').strip() or 'units'
        if not item_name:
            flash('Item name is required.', 'danger')
            return render_template('inventory_form.html', item=None)
        if quantity is None:
            quantity = 0
        item = Inventory(
            item_name=item_name,
            category=category,
            quantity=quantity,
            unit=unit
        )
        db.session.add(item)
        db.session.commit()
        flash('Inventory item added successfully.', 'success')
        return redirect(url_for('inventory.list_items'))
    return render_template('inventory_form.html', item=None)


@inventory_bp.route('/edit/<int:item_id>', methods=['GET', 'POST'])
@login_required
def edit_item(item_id):
    """Edit inventory item (update quantity and details)."""
    item = Inventory.query.get_or_404(item_id)
    if request.method == 'POST':
        item.item_name = request.form.get('item_name', '').strip() or item.item_name
        item.category = request.form.get('category', 'Feed').strip() or item.category
        qty = request.form.get('quantity', type=int)
        if qty is not None:
            item.quantity = qty
        item.unit = request.form.get('unit', 'units').strip() or 'units'
        db.session.commit()
        flash('Inventory item updated successfully.', 'success')
        return redirect(url_for('inventory.list_items'))
    return render_template('inventory_form.html', item=item)


@inventory_bp.route('/delete/<int:item_id>', methods=['POST'])
@login_required
def delete_item(item_id):
    """Delete an inventory item."""
    item = Inventory.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash('Inventory item deleted successfully.', 'success')
    return redirect(url_for('inventory.list_items'))
