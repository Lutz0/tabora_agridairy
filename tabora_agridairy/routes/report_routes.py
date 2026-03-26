"""
Tabora AgriDairy - Reports and Analytics Routes (Controller)
Daily/monthly milk, inventory usage, farmer payments. Chart.js data.
"""
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from database.db import db
from models.cow import Cow
from models.milk import MilkProduction
from models.inventory import Inventory
from models.payment import Payment
from sqlalchemy import func, extract
from datetime import date, timedelta

report_bp = Blueprint('report', __name__)


def get_cow_ids_for_user():
    """Cow IDs for current user (admin: all)."""
    if current_user.is_admin():
        return None  # all
    return [c.id for c in Cow.query.filter_by(owner_id=current_user.id).all()]


@report_bp.route('/')
@login_required
def index():
    """Reports dashboard with charts (Chart.js)."""
    cow_ids = get_cow_ids_for_user()

    # Daily milk (last 14 days) for chart
    start_date = date.today() - timedelta(days=14)
    q = db.session.query(MilkProduction.date, func.sum(MilkProduction.quantity_liters).label('total')).filter(
        MilkProduction.date >= start_date
    )
    if cow_ids is not None:
        if not cow_ids:
            daily_milk = []
        else:
            q = q.filter(MilkProduction.cow_id.in_(cow_ids))
            daily_milk = q.group_by(MilkProduction.date).order_by(MilkProduction.date).all()
    else:
        daily_milk = q.group_by(MilkProduction.date).order_by(MilkProduction.date).all()

    daily_labels = [d.date.strftime('%Y-%m-%d') for d in daily_milk]
    daily_values = [float(d.total) for d in daily_milk]

    # Monthly milk (last 12 months)
    month_start = date.today().replace(day=1)
    twelve_months_ago = (month_start - timedelta(days=1)).replace(day=1)
    y_col = extract('year', MilkProduction.date)
    m_col = extract('month', MilkProduction.date)
    qm = db.session.query(
        y_col.label('y'),
        m_col.label('m'),
        func.sum(MilkProduction.quantity_liters).label('total')
    ).filter(MilkProduction.date >= twelve_months_ago)
    if cow_ids is not None:
        if not cow_ids:
            monthly_data = []
        else:
            qm = qm.filter(MilkProduction.cow_id.in_(cow_ids))
            monthly_data = qm.group_by(y_col, m_col).order_by(y_col, m_col).all()
    else:
        monthly_data = qm.group_by(y_col, m_col).order_by(y_col, m_col).all()

    monthly_labels = [f"{int(m.y)}-{int(m.m):02d}" for m in monthly_data]
    monthly_values = [float(m.total) for m in monthly_data]

    # Inventory by category (for chart)
    inv_by_cat = db.session.query(Inventory.category, func.sum(Inventory.quantity).label('total')).group_by(
        Inventory.category
    ).all()
    inv_labels = [i.category for i in inv_by_cat]
    inv_values = [int(i.total) for i in inv_by_cat]

    # Farmer payments (last 6 months) - admin only for "all farmers"
    pay_start = date.today() - timedelta(days=180)
    py_col = extract('year', Payment.payment_date)
    pm_col = extract('month', Payment.payment_date)
    if current_user.is_admin():
        pay_by_month = db.session.query(
            py_col.label('y'),
            pm_col.label('m'),
            func.sum(Payment.amount).label('total')
        ).filter(Payment.payment_date >= pay_start).group_by(py_col, pm_col).order_by(py_col, pm_col).all()
    else:
        pay_by_month = db.session.query(
            py_col.label('y'),
            pm_col.label('m'),
            func.sum(Payment.amount).label('total')
        ).filter(Payment.payment_date >= pay_start, Payment.farmer_id == current_user.id).group_by(
            py_col, pm_col
        ).order_by(py_col, pm_col).all()
    pay_labels = [f"{int(p.y)}-{int(p.m):02d}" for p in pay_by_month]
    pay_values = [float(p.total) for p in pay_by_month]

    return render_template(
        'reports.html',
        daily_labels=daily_labels,
        daily_values=daily_values,
        monthly_labels=monthly_labels,
        monthly_values=monthly_values,
        inv_labels=inv_labels,
        inv_values=inv_values,
        pay_labels=pay_labels,
        pay_values=pay_values
    )
