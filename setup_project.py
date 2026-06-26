#!/usr/bin/env python
"""
ГДПБЗН Project Setup Script
Run this once to create all files and folders
"""

import os
import sys
from pathlib import Path

# Project root
BASE_DIR = Path(__file__).resolve().parent

# All directories to create
DIRECTORIES = [
    "app/blueprints/auth",
    "app/blueprints/dashboard",
    "app/blueprints/incidents",
    "app/blueprints/teams",
    "app/blueprints/operations",
    "app/blueprints/communications",
    "app/blueprints/resources",
    "app/blueprints/reports",
    "app/models",
    "app/templates/auth",
    "app/templates/dashboard/components",
    "app/templates/incidents/partials",
    "app/templates/teams",
    "app/templates/operations/partials",
    "app/templates/communications",
    "app/templates/resources",
    "app/templates/reports",
    "app/static/css",
    "app/static/js/map",
    "app/static/js/notifications",
    "app/static/js/operations",
    "app/static/js/communication",
    "app/static/js/utils",
    "app/static/images/icons",
    "app/static/images/badges",
    "app/static/images/backgrounds",
    "app/static/vendor",
    "app/forms",
    "app/services",
    "app/api/v1",
    "app/api/mobile",
    "app/utils",
    "app/config",
    "instance",
    "logs",
    "migrations/versions",
    "tests/unit",
    "tests/integration",
    "tests/fixtures",
]

# All files with their content
FILES = {
    # Root files
    "run.py": '''import os
from dotenv import load_dotenv
from app import create_app

load_dotenv()

app = create_app()

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
''',
    
    "config.py": '''import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Database - use absolute path for Windows
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'instance', 'gdpozharna.db').replace('\\\\', '/')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change-in-production'
    SESSION_COOKIE_SECURE = True if os.environ.get('FLASK_ENV') == 'production' else False
    SESSION_COOKIE_HTTPONLY = True
    PERMANENT_SESSION_LIFETIME = 3600
    
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    UPLOAD_FOLDER = 'uploads'
    
    API_TITLE = 'ГДПБЗН API'
    API_VERSION = 'v1'
    
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379/0'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-dev-key'
''',
    
    "requirements.txt": '''# Core Flask
Flask==3.0.2
Flask-SQLAlchemy==3.1.1
Flask-Migrate==4.0.5
Flask-Login==0.6.2
Flask-WTF==1.1.1
Flask-CORS==4.0.0

# Database
psycopg2-binary==2.9.9

# Real-time features
Flask-SocketIO==5.3.6
python-socketio==5.10.0
eventlet==0.33.3

# API
Flask-RESTx==1.2.0
marshmallow==3.20.1

# Authentication & Security
python-dotenv==1.0.0
bcrypt==4.1.2
PyJWT==2.8.0

# Utilities
Pillow==10.2.0
python-dateutil==2.8.2
requests==2.31.0

# Development tools
pytest==7.4.4
pytest-flask==1.2.0
black==23.11.0
flake8==6.1.0

# Map tools
folium==0.15.1
geopy==2.4.1
''',
    
    ".env.example": '''# Flask
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

# Database
DATABASE_URL=sqlite:///instance/gdpozharna.db

# JWT
JWT_SECRET_KEY=your-jwt-secret

# Redis
REDIS_URL=redis://localhost:6379/0

# Map settings
LEAFLET_TILE_LAYER=https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png
''',
    
    "README.md": '''# ГДПБЗН - Система за управление на произшествия

## Описание
Система за управление на произшествия и пожарни екипи за Главна дирекция "Пожарна безопасност и защита на населението".

## Инсталация
1. Създайте виртуална среда: `python -m venv venv`
2. Активирайте я: `venv\\Scripts\\activate` (Windows) или `source venv/bin/activate` (Mac/Linux)
3. Инсталирайте зависимости: `pip install -r requirements.txt`
4. Стартирайте: `python run.py`

## Технологии
- Flask 3.0
- SQLAlchemy
- Bootstrap 5
- Leaflet.js
- Socket.IO
''',
    
    # App __init__.py
    "app/__init__.py": '''from flask import Flask
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
    login_manager.login_message = 'Моля, влезте в системата'
    login_manager.login_message_category = 'warning'
    
    # Register blueprints
    from app.blueprints.auth import auth_bp
    from app.blueprints.dashboard import dashboard_bp
    from app.blueprints.incidents import incidents_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp, url_prefix='/')
    app.register_blueprint(incidents_bp, url_prefix='/incidents')
    
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Resource not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return {'error': 'Internal server error'}, 500
    
    @app.route('/test')
    def test():
        return "ГДПБЗН системата работи! 🚒"
    
    with app.app_context():
        db.create_all()
    
    return app
''',
    
    # Auth blueprint
    "app/blueprints/auth/__init__.py": '''from flask import Blueprint

auth_bp = Blueprint('auth', __name__, template_folder='templates')

from . import routes
''',
    
    "app/blueprints/auth/routes.py": '''from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import auth_bp

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Успешно излязохте от системата', 'success')
    return redirect(url_for('auth.login'))
''',
    
    "app/blueprints/auth/forms.py": '''from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(FlaskForm):
    email = StringField('Имейл', validators=[DataRequired(), Email()])
    password = PasswordField('Парола', validators=[DataRequired(), Length(min=6)])
    remember = BooleanField('Запомни ме')
    submit = SubmitField('Вход')
''',
    
    # Dashboard blueprint
    "app/blueprints/dashboard/__init__.py": '''from flask import Blueprint

dashboard_bp = Blueprint('dashboard', __name__, template_folder='templates')

from . import routes
''',
    
    "app/blueprints/dashboard/routes.py": '''from flask import render_template
from flask_login import login_required
from . import dashboard_bp

@dashboard_bp.route('/')
@login_required
def index():
    return render_template('dashboard/index.html', title='Табло')

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard/index.html', title='Табло')
''',
    
    "app/blueprints/dashboard/forms.py": '''from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField

class DashboardFilterForm(FlaskForm):
    date_range = SelectField('Период', choices=[('today', 'Днес'), ('week', 'Седмица'), ('month', 'Месец')])
    submit = SubmitField('Приложи')
''',
    
    # Incidents blueprint
    "app/blueprints/incidents/__init__.py": '''from flask import Blueprint

incidents_bp = Blueprint('incidents', __name__, template_folder='templates')

from . import routes
''',
    
    "app/blueprints/incidents/routes.py": '''from flask import render_template, jsonify, request
from flask_login import login_required
from . import incidents_bp

@incidents_bp.route('/')
@login_required
def list_incidents():
    return render_template('incidents/list.html', title='Произшествия')

@incidents_bp.route('/create')
@login_required
def create_incident():
    return render_template('incidents/create.html', title='Ново произшествие')

@incidents_bp.route('/api/test')
def api_test():
    return jsonify({'status': 'OK', 'message': 'API работи!'})
''',
    
    "app/blueprints/incidents/forms.py": '''from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, FloatField, SubmitField
from wtforms.validators import DataRequired, Optional

class IncidentForm(FlaskForm):
    title = StringField('Заглавие', validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[DataRequired()])
    type = SelectField('Тип', choices=[('fire', 'Пожар'), ('rescue', 'Спасителна'), ('other', 'Друго')])
    address = StringField('Адрес', validators=[DataRequired()])
    latitude = FloatField('Географска ширина', validators=[Optional()])
    longitude = FloatField('Географска дължина', validators=[Optional()])
    submit = SubmitField('Запази')
''',
    
    "app/blueprints/incidents/services.py": '''from app import db
from app.models.incident import Incident

class IncidentService:
    @staticmethod
    def create_incident(data):
        incident = Incident(**data)
        db.session.add(incident)
        db.session.commit()
        return incident
    
    @staticmethod
    def get_incident(incident_id):
        return Incident.query.get(incident_id)
    
    @staticmethod
    def get_all_incidents():
        return Incident.query.all()
''',
    
    # Templates
    "app/templates/base.html": '''<!DOCTYPE html>
<html lang="bg">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ГДПБЗН - {% block title %}Система за управление{% endblock %}</title>
    
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <style>
        body { background-color: #f8f9fa; }
        .navbar-brand { font-weight: bold; }
        .alert { margin-top: 20px; }
        .bg-danger-custom { background-color: #dc3545; }
    </style>
    {% block extra_css %}{% endblock %}
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-danger">
        <div class="container-fluid">
            <a class="navbar-brand" href="{{ url_for('dashboard.index') }}">
                <i class="fas fa-fire-extinguisher"></i> ГДПБЗН
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    {% if current_user.is_authenticated %}
                        <li class="nav-item"><span class="nav-link"><i class="fas fa-user"></i> {{ current_user.name }}</span></li>
                        <li class="nav-item"><a class="nav-link" href="{{ url_for('auth.logout') }}"><i class="fas fa-sign-out-alt"></i> Изход</a></li>
                    {% else %}
                        <li class="nav-item"><a class="nav-link" href="{{ url_for('auth.login') }}"><i class="fas fa-sign-in-alt"></i> Вход</a></li>
                    {% endif %}
                </ul>
            </div>
        </div>
    </nav>

    <div class="container mt-3">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }} alert-dismissible fade show" role="alert">
                        {{ message }}
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}
    </div>

    <main class="container mt-4">
        {% block content %}{% endblock %}
    </main>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://cdn.socket.io/4.7.2/socket.io.min.js"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
''',
    
    "app/templates/auth/login.html": '''{% extends "base.html" %}
{% block title %}Вход{% endblock %}
{% block content %}
<div class="row justify-content-center mt-5">
    <div class="col-md-6 col-lg-4">
        <div class="card shadow">
            <div class="card-header bg-danger text-white text-center">
                <h4><i class="fas fa-fire-extinguisher"></i> ГДПБЗН</h4>
                <p class="mb-0">Вход в системата</p>
            </div>
            <div class="card-body">
                <form method="POST">
                    <div class="mb-3">
                        <label for="email" class="form-label">Имейл</label>
                        <input type="email" class="form-control" id="email" name="email" required>
                    </div>
                    <div class="mb-3">
                        <label for="password" class="form-label">Парола</label>
                        <input type="password" class="form-control" id="password" name="password" required>
                    </div>
                    <button type="submit" class="btn btn-danger w-100">
                        <i class="fas fa-sign-in-alt"></i> Вход
                    </button>
                </form>
                <div class="mt-3 text-center">
                    <small class="text-muted">Тест: admin@example.com / admin123</small>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
''',
    
    "app/templates/dashboard/index.html": '''{% extends "base.html" %}
{% block title %}Табло{% endblock %}
{% block content %}
<div class="row">
    <div class="col-12">
        <h1 class="display-4">Добре дошли в ГДПБЗН</h1>
        <p class="lead">Система за управление на произшествия и пожарни екипи</p>
        <hr>
    </div>
</div>
<div class="row mt-4">
    <div class="col-md-3 col-sm-6 mb-3">
        <div class="card bg-primary text-white">
            <div class="card-body">
                <h5 class="card-title">Активни произшествия</h5>
                <h2 class="display-4">0</h2>
            </div>
        </div>
    </div>
    <div class="col-md-3 col-sm-6 mb-3">
        <div class="card bg-success text-white">
            <div class="card-body">
                <h5 class="card-title">Налични екипи</h5>
                <h2 class="display-4">0</h2>
            </div>
        </div>
    </div>
    <div class="col-md-3 col-sm-6 mb-3">
        <div class="card bg-warning text-white">
            <div class="card-body">
                <h5 class="card-title">На служба</h5>
                <h2 class="display-4">0</h2>
            </div>
        </div>
    </div>
    <div class="col-md-3 col-sm-6 mb-3">
        <div class="card bg-danger text-white">
            <div class="card-body">
                <h5 class="card-title">Спешни сигнали</h5>
                <h2 class="display-4">0</h2>
            </div>
        </div>
    </div>
</div>
<div class="row mt-4">
    <div class="col-12">
        <div class="card">
            <div class="card-header"><i class="fas fa-clock"></i> Последна активност</div>
            <div class="card-body">
                <p class="text-muted">Все още няма активност в системата.</p>
            </div>
        </div>
    </div>
</div>
{% endblock %}
''',
    
    "app/templates/incidents/list.html": '''{% extends "base.html" %}
{% block title %}Произшествия{% endblock %}
{% block content %}
<div class="row">
    <div class="col-12">
        <h1>Произшествия</h1>
        <p class="lead">Списък на всички регистрирани произшествия</p>
        <hr>
    </div>
</div>
<div class="row mt-4">
    <div class="col-12">
        <div class="alert alert-info">
            <i class="fas fa-info-circle"></i> Все още няма регистрирани произшествия.
        </div>
        <a href="{{ url_for('incidents.create_incident') }}" class="btn btn-danger">
            <i class="fas fa-plus"></i> Ново произшествие
        </a>
    </div>
</div>
{% endblock %}
''',
    
    "app/templates/incidents/create.html": '''{% extends "base.html" %}
{% block title %}Ново произшествие{% endblock %}
{% block content %}
<div class="row">
    <div class="col-12">
        <h1>Ново произшествие</h1>
        <hr>
    </div>
</div>
<div class="row mt-4">
    <div class="col-md-8">
        <div class="card">
            <div class="card-body">
                <form>
                    <div class="mb-3">
                        <label class="form-label">Тип произшествие</label>
                        <select class="form-select">
                            <option>Пожар</option>
                            <option>Спасителна операция</option>
                            <option>Друго</option>
                        </select>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Адрес</label>
                        <input type="text" class="form-control" placeholder="Въведете адрес">
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Описание</label>
                        <textarea class="form-control" rows="3"></textarea>
                    </div>
                    <button type="submit" class="btn btn-danger">
                        <i class="fas fa-save"></i> Запази
                    </button>
                </form>
            </div>
        </div>
    </div>
    <div class="col-md-4">
        <div class="card">
            <div class="card-header">Карта</div>
            <div class="card-body">
                <div id="map" style="height: 300px; background: #e9ecef; display: flex; align-items: center; justify-content: center;">
                    <span class="text-muted">Карта ще се зареди тук</span>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
''',
}

def create_structure():
    """Create all directories and files"""
    print("🚒 Създаване на структурата на проекта...")
    
    # Create directories
    for directory in DIRECTORIES:
        dir_path = BASE_DIR / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"  📁 Създадена папка: {directory}")
    
    # Create files
    for file_path, content in FILES.items():
        file_full_path = BASE_DIR / file_path
        file_full_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  📄 Създаден файл: {file_path}")
    
    # Create __init__.py in all blueprint folders
    blueprint_dirs = [
        "app/blueprints/teams",
        "app/blueprints/operations",
        "app/blueprints/communications",
        "app/blueprints/resources",
        "app/blueprints/reports",
    ]
    for bdir in blueprint_dirs:
        init_file = BASE_DIR / bdir / "__init__.py"
        if not init_file.exists():
            with open(init_file, 'w', encoding='utf-8') as f:
                f.write('''from flask import Blueprint

bp = Blueprint('{}', __name__, template_folder='templates')

from . import routes
'''.format(bdir.split('/')[-1]))
            print(f"  📄 Създаден __init__.py: {bdir}")
    
    # Create __init__.py in other folders
    init_folders = [
        "app/models",
        "app/forms",
        "app/services",
        "app/api/v1",
        "app/api/mobile",
        "app/utils",
        "app/config",
        "tests/unit",
        "tests/integration",
        "tests/fixtures",
    ]
    for folder in init_folders:
        init_file = BASE_DIR / folder / "__init__.py"
        if not init_file.exists():
            with open(init_file, 'w', encoding='utf-8') as f:
                f.write('# This file makes the folder a Python package\n')
            print(f"  📄 Създаден __init__.py: {folder}")
    
    # Create .env file from example
    env_example = BASE_DIR / ".env.example"
    env_file = BASE_DIR / ".env"
    if env_example.exists() and not env_file.exists():
        import shutil
        shutil.copy(env_example, env_file)
        print("  📄 Създаден .env от .env.example")
    
    # Create empty instance/db file
    db_file = BASE_DIR / "instance" / "gdpozharna.db"
    if not db_file.exists():
        import sqlite3
        conn = sqlite3.connect(str(db_file))
        conn.close()
        print(f"  🗄️  Създадена база данни: {db_file}")
    
    print("\n✅ Проектът е създаден успешно!")
    print("\n📋 Следващи стъпки:")
    print("  1. Активирайте виртуалната среда: venv\\Scripts\\activate")
    print("  2. Инсталирайте зависимости: pip install -r requirements.txt")
    print("  3. Стартирайте: python run.py")
    print("  4. Отворете: http://localhost:5000/test")

if __name__ == "__main__":
    create_structure()