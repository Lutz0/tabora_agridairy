"""
Tabora AgriDairy - Settings Routes
Basic farm settings management.
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from database.db import db
from models.setting import Setting


settings_bp = Blueprint('settings', __name__)


def get_setting_value(key, default=''):
    row = Setting.query.filter_by(key=key).first()
    return row.value if row else default


def set_setting_value(key, value):
    row = Setting.query.filter_by(key=key).first()
    if not row:
        row = Setting(key=key, value=value)
        db.session.add(row)
    else:
        row.value = value


@settings_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    """Display and update farm settings."""
    if not current_user.is_admin():
        flash('Only administrators can update settings.', 'danger')
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        farm_name = request.form.get('farm_name', '').strip()
        admin_email = request.form.get('admin_email', '').strip()
        notifications_enabled = '1' if request.form.get('notifications_enabled') == 'on' else '0'

        if not farm_name or not admin_email:
            flash('Farm name and admin email are required.', 'danger')
            return render_template('settings.html',
                                   farm_name=farm_name,
                                   admin_email=admin_email,
                                   notifications_enabled=(notifications_enabled == '1')), 400

        set_setting_value('farm_name', farm_name)
        set_setting_value('admin_email', admin_email)
        set_setting_value('notifications_enabled', notifications_enabled)
        db.session.commit()
        flash('Settings updated successfully.', 'success')
        return redirect(url_for('settings.settings'))

    return render_template(
        'settings.html',
        farm_name=get_setting_value('farm_name', 'Tabora Dairy Farm'),
        admin_email=get_setting_value('admin_email', ''),
        notifications_enabled=get_setting_value('notifications_enabled', '1') == '1'
    )

