from flask import render_template
from flask_login import login_required, current_user
from . import dashboard_bp
from app import db
from app.models.incident import Incident
from app.models.team import Team
from app.models.user import User
from sqlalchemy import func
from app.utils.decorators import staff_required  # ADD THIS IMPORT

@dashboard_bp.route('/dashboard')
@login_required
@staff_required
def index():
    # Stats
    total_incidents = Incident.query.count()
    active_incidents = Incident.query.filter(Incident.status.in_(['active', 'in_progress'])).count()
    resolved_incidents = Incident.query.filter_by(status='resolved').count()
    
    # Resolution stats
    total_lives_saved = db.session.query(func.sum(Incident.lives_saved)).filter_by(status='resolved').scalar() or 0
    total_deaths = db.session.query(func.sum(Incident.deaths)).filter_by(status='resolved').scalar() or 0
    
    # Success rate calculation
    success_count = Incident.query.filter_by(status='resolved', outcome='success').count()
    success_rate = round((success_count / resolved_incidents * 100) if resolved_incidents > 0 else 0, 1)
    
    # Active incidents list
    active_incidents_list = Incident.query.filter(Incident.status.in_(['active', 'in_progress'])).order_by(Incident.created_at.desc()).limit(5).all()
    
    # Teams status
    teams = Team.query.all()
    
    # Recent activity
    recent_activity = Incident.query.order_by(Incident.created_at.desc()).limit(5).all()
    
    return render_template(
        'dashboard/index.html',
        title='Табло',
        total_incidents=total_incidents,
        active_incidents=active_incidents,
        resolved_incidents=resolved_incidents,
        total_lives_saved=total_lives_saved,
        total_deaths=total_deaths,
        success_rate=success_rate,
        active_incidents_list=active_incidents_list,
        teams=teams,
        recent_activity=recent_activity
    )