"""
Tabora AgriDairy - Dashboard Routes (Controller)
Shows overview: total farmers, milk collected today, monthly revenue, inventory alerts.
"""
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from database.db import db
from models.cow import Cow
from models.milk import MilkProduction
from models.inventory import Inventory
from models.payment import Payment
from models.user import User
from sqlalchemy import func
from datetime import date, timedelta

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/')
@login_required
def index():
    """Dashboard home: KPI cards, trend chart, and daily tables."""
    today = date.today()

    # Scope (admin: all data; farmer: own data)
    if current_user.is_admin():
        cow_ids = None
        total_farmers = User.query.filter_by(role='farmer').count()
        recent_payments = Payment.query.order_by(Payment.payment_date.desc()).limit(5).all()
    else:
        # All cows owned by the current farmer (IDs only)
        cow_ids = [c.id for c in Cow.query.filter_by(owner_id=current_user.id).all()]
        total_farmers = 1  # current farmer account
        recent_payments = Payment.query.filter_by(farmer_id=current_user.id).order_by(
            Payment.payment_date.desc()
        ).limit(5).all()

    # Today's milk collected
    if cow_ids is None:
        milk_today = db.session.query(func.coalesce(func.sum(MilkProduction.quantity_liters), 0)).filter(
            MilkProduction.date == today
        ).scalar() or 0
    elif not cow_ids:
        milk_today = 0
    else:
        milk_today = db.session.query(func.coalesce(func.sum(MilkProduction.quantity_liters), 0)).filter(
            MilkProduction.date == today,
            MilkProduction.cow_id.in_(cow_ids)
        ).scalar() or 0

    # Monthly revenue (payments in current month)
    first_of_month = today.replace(day=1)
    monthly_revenue = db.session.query(func.coalesce(func.sum(Payment.amount), 0)).filter(
        Payment.payment_date >= first_of_month,
        Payment.payment_date <= today,
        *( [Payment.farmer_id == current_user.id] if not current_user.is_admin() else [] )
    ).scalar()
    monthly_revenue = monthly_revenue or 0

    # Inventory alerts (low stock)
    low_stock_threshold = 10
    inventory_alerts = Inventory.query.filter(Inventory.quantity <= low_stock_threshold).count()

    # Daily milk records table (today)
    records_q = MilkProduction.query.filter(MilkProduction.date == today).order_by(MilkProduction.id.desc())
    if cow_ids is not None:
        records_q = records_q.filter(MilkProduction.cow_id.in_(cow_ids)) if cow_ids else records_q.filter(False)
    today_records = records_q.limit(10).all()

    # 7-day milk trend (labels + values)
    # Compute dates in Python and query with IN for portability.
    last_7_days = [today - timedelta(days=i) for i in range(6, -1, -1)]
    tq = db.session.query(MilkProduction.date, func.sum(MilkProduction.quantity_liters).label('total')).filter(
        MilkProduction.date.in_(last_7_days)
    )
    if cow_ids is not None:
        tq = tq.filter(MilkProduction.cow_id.in_(cow_ids)) if cow_ids else tq.filter(False)
    trend_rows = tq.group_by(MilkProduction.date).order_by(MilkProduction.date).all()
    trend_map = {r.date.strftime('%Y-%m-%d'): float(r.total) for r in trend_rows}
    trend_labels = [d.strftime('%Y-%m-%d') for d in last_7_days]
    trend_values = [round(trend_map.get(lbl, 0.0), 2) for lbl in trend_labels]

    return render_template(
        'dashboard.html',
        total_farmers=total_farmers,
        milk_today=round(milk_today, 2),
        monthly_revenue=round(monthly_revenue, 2),
        inventory_alerts=inventory_alerts,
        today_records=today_records,
        trend_labels=trend_labels,
        trend_values=trend_values,
        recent_payments=recent_payments
    )
