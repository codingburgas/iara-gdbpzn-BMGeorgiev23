from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from . import incidents_bp
from app import db
from app.models.incident import Incident
from app.models.team import Team
from app.models.user import User

@incidents_bp.route('/')
@login_required
def list_incidents():
    incidents = Incident.query.order_by(Incident.created_at.desc()).all()
    return render_template('incidents/list.html', title='Произшествия', incidents=incidents)

@incidents_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_incident():
    teams = Team.query.all()
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        incident_type = request.form.get('type')
        address = request.form.get('address')
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        priority = request.form.get('priority', 'medium')
        assigned_team_id = request.form.get('assigned_team_id')
        
        if not title or not address:
            flash('Заглавието и адресът са задължителни.', 'danger')
            return render_template('incidents/create.html', teams=teams)
        
        incident = Incident(
            title=title,
            description=description,
            type=incident_type,
            address=address,
            latitude=float(latitude) if latitude else None,
            longitude=float(longitude) if longitude else None,
            priority=priority,
            assigned_team_id=int(assigned_team_id) if assigned_team_id else None,
            created_by_id=current_user.id
        )
        
        db.session.add(incident)
        db.session.commit()
        
        flash('Произшествието е създадено успешно.', 'success')
        return redirect(url_for('incidents.list_incidents'))
    
    return render_template('incidents/create.html', teams=teams)

@incidents_bp.route('/<int:incident_id>')
@login_required
def detail_incident(incident_id):
    incident = Incident.query.get_or_404(incident_id)
    return render_template('incidents/detail.html', title='Детайли', incident=incident)

@incidents_bp.route('/<int:incident_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_incident(incident_id):
    incident = Incident.query.get_or_404(incident_id)
    teams = Team.query.all()
    
    if request.method == 'POST':
        incident.title = request.form.get('title')
        incident.description = request.form.get('description')
        incident.type = request.form.get('type')
        incident.address = request.form.get('address')
        incident.latitude = float(request.form.get('latitude')) if request.form.get('latitude') else None
        incident.longitude = float(request.form.get('longitude')) if request.form.get('longitude') else None
        incident.priority = request.form.get('priority')
        incident.status = request.form.get('status')
        incident.assigned_team_id = int(request.form.get('assigned_team_id')) if request.form.get('assigned_team_id') else None
        incident.updated_at = datetime.utcnow()
        
        if incident.status == 'resolved' and not incident.resolved_at:
            incident.resolved_at = datetime.utcnow()
        
        db.session.commit()
        flash('Произшествието е обновено успешно.', 'success')
        return redirect(url_for('incidents.detail_incident', incident_id=incident.id))
    
    return render_template('incidents/edit.html', title='Редактиране', incident=incident, teams=teams)

@incidents_bp.route('/<int:incident_id>/delete', methods=['POST'])
@login_required
def delete_incident(incident_id):
    incident = Incident.query.get_or_404(incident_id)
    db.session.delete(incident)
    db.session.commit()
    flash('Произшествието е изтрито.', 'success')
    return redirect(url_for('incidents.list_incidents'))

@incidents_bp.route('/api/data')
@login_required
def api_incidents_data():
    incidents = Incident.query.all()
    data = []
    for incident in incidents:
        data.append({
            'id': incident.id,
            'title': incident.title,
            'type': incident.get_type_display(),
            'status': incident.get_status_display(),
            'priority': incident.get_priority_display(),
            'address': incident.address,
            'created_at': incident.created_at.strftime('%Y-%m-%d %H:%M'),
            'assigned_team': incident.assigned_team.name if incident.assigned_team else 'Не е назначен'
        })
    return jsonify(data)

@incidents_bp.route('/<int:incident_id>/update-status', methods=['POST'])
@login_required
def update_status(incident_id):
    incident = Incident.query.get_or_404(incident_id)
    status = request.json.get('status')
    
    if status in ['active', 'in_progress', 'resolved', 'closed']:
        incident.status = status
        if status == 'resolved' and not incident.resolved_at:
            incident.resolved_at = datetime.utcnow()
        db.session.commit()
        return jsonify({'success': True, 'status': incident.get_status_display()})
    
    return jsonify({'success': False, 'error': 'Invalid status'}), 400