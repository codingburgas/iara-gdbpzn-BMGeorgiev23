from flask import render_template, redirect, url_for
from flask_login import current_user, login_required
from . import main_bp
from app.models.incident import Incident

@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        # Redirect based on role
        if current_user.is_admin() or current_user.is_firefighter():
            return redirect(url_for('dashboard.index'))
        else:
            # Regular users get their own dashboard
            return redirect(url_for('main.user_dashboard'))
    return render_template('main/index.html', title='Начало')

@main_bp.route('/about')
def about():
    return render_template('main/about.html', title='За нас')

@main_bp.route('/contact')
def contact():
    return render_template('main/contact.html', title='Контакти')

@main_bp.route('/report')
@login_required
def report():
    return render_template('main/report.html', title='Докладвай произшествие')

@main_bp.route('/my-reports')
@login_required
def my_reports():
    incidents = Incident.query.filter_by(created_by_id=current_user.id).order_by(Incident.created_at.desc()).all()
    return render_template('main/my_reports.html', title='Моите доклади', incidents=incidents)

@main_bp.route('/user-dashboard')
@login_required
def user_dashboard():
    incidents = Incident.query.filter_by(created_by_id=current_user.id).order_by(Incident.created_at.desc()).all()
    return render_template('main/user_dashboard.html', title='Моят профил', incidents=incidents)