from flask import render_template, jsonify, request
from flask_login import login_required
from datetime import datetime
from . import operations_bp
from app import db
from app.models.incident import Incident
from app.models.team import Team
from app.models.user import User
from app.utils.decorators import staff_required, role_required

@operations_bp.route('/')
@login_required
@staff_required
def live():
    incidents = Incident.query.filter(Incident.status.in_(['active', 'in_progress'])).all()
    # Get all teams, filter in Python using the property
    all_teams = Team.query.all()
    teams = [team for team in all_teams if team.get_status() == 'available']
    now = datetime.now()
    return render_template('operations/live.html', title='Оперативен център', incidents=incidents, teams=teams, now=now)

@operations_bp.route('/tasks')
@login_required
@staff_required
def task_board():
    incidents = Incident.query.order_by(Incident.created_at.desc()).all()
    return render_template('operations/task_board.html', title='Табло за задачи', incidents=incidents)

@operations_bp.route('/map')
@login_required
@staff_required
def map_control():
    incidents = Incident.query.all()
    teams = Team.query.all()
    return render_template('operations/map_control.html', title='Карта', incidents=incidents, teams=teams)

@operations_bp.route('/api/incidents')
@login_required
@staff_required
def api_incidents():
    incidents = Incident.query.all()
    data = []
    for incident in incidents:
        data.append({
            'id': incident.id,
            'title': incident.title,
            'type': incident.type,
            'status': incident.status,
            'priority': incident.priority,
            'latitude': incident.latitude,
            'longitude': incident.longitude,
            'address': incident.address,
            'created_at': incident.created_at.isoformat()
        })
    return jsonify(data)

@operations_bp.route('/api/teams')
@login_required
@staff_required
def api_teams():
    teams = Team.query.all()
    data = []
    for team in teams:
        data.append({
            'id': team.id,
            'name': team.name,
            'status': team.get_status_display(),
            'member_count': len(team.members)
        })
    return jsonify(data)