"""
Tabora AgriDairy Management System
Main Flask application entry point.
MVC Architecture: routes (controllers), models, templates (views).
"""
import os
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from sqlalchemy import inspect, text
from sqlalchemy.exc import OperationalError

from config import Config
from database.db import db


def create_app(config_class=Config):
    """Application factory: create and configure the Flask app."""
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config.from_object(config_class)
    _validate_runtime_environment(app)

    # Initialize extensions
    db.init_app(app)
    migrate = Migrate()
    migrate.init_app(app, db)

    # Flask-Login setup
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'

    from models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from routes.auth_routes import auth_bp
    from routes.cow_routes import cow_bp
    from routes.milk_routes import milk_bp
    from routes.inventory_routes import inventory_bp
    from routes.payment_routes import payment_bp
    from routes.report_routes import report_bp
    from routes.health_routes import health_bp
    from routes.settings_routes import settings_bp

    # Import all models before create_all so new tables are detected
    import models  # noqa: F401

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(cow_bp, url_prefix='/cows')
    app.register_blueprint(milk_bp, url_prefix='/milk')
    app.register_blueprint(inventory_bp, url_prefix='/inventory')
    app.register_blueprint(payment_bp, url_prefix='/payments')
    app.register_blueprint(report_bp, url_prefix='/reports')
    app.register_blueprint(health_bp)
    app.register_blueprint(settings_bp)

    # Create database tables (use Flask-Migrate in production for migrations)
    with app.app_context():
        try:
            db.create_all()
            _ensure_payment_schema_compatibility()
        except OperationalError as exc:
            app.logger.exception("Database initialization failed.")
            raise

    # Root redirect to dashboard or login
    @app.route('/')
    def index():
        from flask import redirect, url_for
        from flask_login import current_user
        if current_user.is_authenticated:
            return redirect(url_for('dashboard.index'))
        return redirect(url_for('auth.login'))

    # Convenience aliases requested by UI spec
    @app.route('/add_cow')
    def add_cow_alias():
        from flask import redirect, url_for
        return redirect(url_for('cow.add_cow'))

    @app.route('/cows')
    def cows_alias():
        from flask import redirect, url_for
        return redirect(url_for('cow.list_cows'))

    @app.route('/edit_cow/<int:cow_id>')
    def edit_cow_alias(cow_id):
        from flask import redirect, url_for
        return redirect(url_for('cow.edit_cow', cow_id=cow_id))

    @app.route('/add_payment')
    def add_payment_alias():
        from flask import redirect, url_for
        return redirect(url_for('payment.add_payment'))

    @app.route('/payments')
    def payments_alias():
        from flask import redirect, url_for
        return redirect(url_for('payment.list_payments'))

    @app.route('/healthz')
    def healthz():
        """Simple health endpoint for Render checks."""
        try:
            db.session.execute(text('SELECT 1'))
            return {'status': 'ok'}, 200
        except Exception:
            return {'status': 'db_unavailable'}, 503

    # Register dashboard as blueprint for consistency
    from routes.dashboard_routes import dashboard_bp
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')

    @app.errorhandler(OperationalError)
    def handle_db_operational_error(error):
        app.logger.error("OperationalError: %s", error)
        return "Database connection error. Check DATABASE_URL and DB service.", 500

    return app


def _validate_runtime_environment(app):
    """Log useful warnings for production deployments."""
    if not os.environ.get('DATABASE_URL'):
        app.logger.warning("DATABASE_URL is not set; using fallback local MySQL configuration.")
    if not os.environ.get('SECRET_KEY'):
        app.logger.warning("SECRET_KEY is not set; using development fallback secret key.")


def _ensure_payment_schema_compatibility():
    """
    Safety patch for existing databases that predate new Payment columns.
    Prevents runtime errors like:
    Unknown column 'payments.payment_method' in 'field list'
    """
    inspector = inspect(db.engine)
    try:
        columns = {col['name'] for col in inspector.get_columns('payments')}
    except Exception as exc:
        # Table may not exist yet in a fresh DB; create_all handles table creation.
        db.session.rollback()
        return

    statements = []
    if 'payment_method' not in columns:
        statements.append(
            "ALTER TABLE payments ADD COLUMN payment_method VARCHAR(20) NOT NULL DEFAULT 'Cash'"
        )
    if 'reference' not in columns:
        statements.append(
            "ALTER TABLE payments ADD COLUMN reference VARCHAR(120) NULL"
        )
    if 'description' not in columns:
        statements.append(
            "ALTER TABLE payments ADD COLUMN description TEXT NULL"
        )

    if statements:
        for sql in statements:
            db.session.execute(text(sql))
        db.session.commit()


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=app.config['DEBUG'])
