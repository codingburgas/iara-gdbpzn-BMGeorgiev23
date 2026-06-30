from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_cors import CORS
import os

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
socketio = SocketIO()
cors = CORS()

def create_app(config_object='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_object)
    
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    socketio.init_app(app)
    cors.init_app(app)
    
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Моля, влезте в системата.'
    login_manager.login_message_category = 'warning'
    
    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return User.query.get(int(user_id))
    
    # Register all blueprints
    from app.blueprints.main import main_bp
    from app.blueprints.auth import auth_bp
    from app.blueprints.dashboard import dashboard_bp
    from app.blueprints.incidents import incidents_bp
    from app.blueprints.teams import teams_bp
    from app.blueprints.operations import operations_bp
    from app.blueprints.communications import communications_bp
    from app.blueprints.resources import resources_bp
    from app.blueprints.reports import reports_bp
    from app.blueprints.admin import admin_bp
    
    app.register_blueprint(main_bp, url_prefix='/')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp, url_prefix='/')
    app.register_blueprint(incidents_bp, url_prefix='/incidents')
    app.register_blueprint(teams_bp, url_prefix='/teams')
    app.register_blueprint(operations_bp, url_prefix='/operations')
    app.register_blueprint(communications_bp, url_prefix='/communications')
    app.register_blueprint(resources_bp, url_prefix='/resources')
    app.register_blueprint(reports_bp, url_prefix='/reports')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Resource not found'}, 404
    
    @app.errorhandler(403)
    def forbidden(error):
        return {'error': 'Access denied'}, 403
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return {'error': 'Internal server error'}, 500
    
    @app.route('/test')
    def test():
        return "ГДПБЗН системата работи!"
    
    with app.app_context():
        db.create_all()
        
        # Seed admin user
        from app.models.user import User
        if not User.query.filter_by(email='admin@example.com').first():
            admin = User(
                email='admin@example.com',
                name='Admin',
                role='admin',
                is_active=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            print('Admin user created: admin@example.com')
        
        # Seed firefighter user
        if not User.query.filter_by(email='firefighter@example.com').first():
            firefighter = User(
                email='firefighter@example.com',
                name='Firefighter',
                role='firefighter',
                is_active=True
            )
            firefighter.set_password('fire123')
            db.session.add(firefighter)
            print('Firefighter user created: firefighter@example.com')
        
        # Seed dispatcher user
        if not User.query.filter_by(email='dispatcher@example.com').first():
            dispatcher = User(
                email='dispatcher@example.com',
                name='Dispatcher',
                role='dispatcher',
                is_active=True
            )
            dispatcher.set_password('disp123')
            db.session.add(dispatcher)
            print('Dispatcher user created: dispatcher@example.com')
        
        # Seed incident manager user
        if not User.query.filter_by(email='manager@example.com').first():
            manager = User(
                email='manager@example.com',
                name='Incident Manager',
                role='incident_manager',
                is_active=True
            )
            manager.set_password('man123')
            db.session.add(manager)
            print('Incident Manager user created: manager@example.com')
        
        db.session.commit()
    
    return app