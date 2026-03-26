"""
Tabora AgriDairy Management System
Main Flask application entry point.
MVC Architecture: routes (controllers), models, templates (views).
"""
import os
from flask import Flask
from flask_login import LoginManager

from config import Config
from database.db import db


def create_app(config_class=Config):
    """Application factory: create and configure the Flask app."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)

    # Flask-Login setup
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'

    from models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Create database tables (use Flask-Migrate in production for migrations)
    with app.app_context():
        db.create_all()

    # Register blueprints
    from routes.auth_routes import auth_bp
    from routes.cow_routes import cow_bp
    from routes.milk_routes import milk_bp
    from routes.inventory_routes import inventory_bp
    from routes.payment_routes import payment_bp
    from routes.report_routes import report_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(cow_bp, url_prefix='/cows')
    app.register_blueprint(milk_bp, url_prefix='/milk')
    app.register_blueprint(inventory_bp, url_prefix='/inventory')
    app.register_blueprint(payment_bp, url_prefix='/payments')
    app.register_blueprint(report_bp, url_prefix='/reports')

    # Root redirect to dashboard or login
    @app.route('/')
    def index():
        from flask import redirect, url_for
        from flask_login import current_user
        if current_user.is_authenticated:
            return redirect(url_for('dashboard.index'))
        return redirect(url_for('auth.login'))

    # Register dashboard as blueprint for consistency
    from routes.dashboard_routes import dashboard_bp
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=app.config['DEBUG'])
