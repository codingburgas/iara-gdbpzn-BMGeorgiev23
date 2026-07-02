from flask import render_template, redirect, url_for, flash, request, jsonify, current_app
from flask_login import login_required, current_user
from datetime import datetime
from werkzeug.utils import secure_filename
import os
from . import incidents_bp
from app import db
from app.models.incident import Incident
from app.models.team import Team
from app.models.user import User
from app.models.warning import Warning
from app.utils.decorators import role_required, staff_required

@incidents_bp.route('/')
@login_required
@staff_required
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
        
        if incident_type == 'other' and not description:
            flash('При избор на "Друго", описанието е задължително.', 'danger')
            return render_template('incidents/create.html', teams=teams)
        
        incident = Incident(
            title=title,
            description=description,
            type=incident_type,
            address=address,
            latitude=float(latitude) if latitude else None,
            longitude=float(longitude) if longitude else None,
            priority=priority,
            assigned_team_id=int(assigned_team_id) if assigned_team_id and current_user.is_staff() else None,
            created_by_id=current_user.id
        )
        
        # Handle file upload
        if 'attachment' in request.files:
            file = request.files['attachment']
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
                new_filename = f'incident_{datetime.utcnow().timestamp()}.{ext}'
                
                upload_dir = os.path.join(current_app.root_path, 'static', 'uploads')
                if not os.path.exists(upload_dir):
                    os.makedirs(upload_dir)
                
                file_path = os.path.join(upload_dir, new_filename)
                file.save(file_path)
                
                incident.attachment_filename = filename
                incident.attachment_path = f'/static/uploads/{new_filename}'
        
        if incident.assigned_team_id:
            incident.status = 'active'
        else:
            incident.status = 'awaiting_assignment'
        
        db.session.add(incident)
        db.session.commit()
        
        flash('Произшествието е създадено успешно.', 'success')
        
        if current_user.is_staff():
            return redirect(url_for('incidents.list_incidents'))
        else:
            return redirect(url_for('main.my_reports'))
    
    return render_template('incidents/create.html', teams=teams)

@incidents_bp.route('/<int:incident_id>')
@login_required
@staff_required
def detail_incident(incident_id):
    incident = Incident.query.get_or_404(incident_id)
    return render_template('incidents/detail.html', title='Детайли', incident=incident)

@incidents_bp.route('/<int:incident_id>/edit', methods=['GET', 'POST'])
@login_required
@staff_required
def edit_incident(incident_id):
    incident = Incident.query.get_or_404(incident_id)
    teams = Team.query.all()
    
    if request.method == 'POST':
        incident.title = request.form.get('title')
        incident.description = request.form.get('description')
        incident.type = request.form.get('type')
        incident.address = request.form.get('address')
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
@role_required(['admin'])
def delete_incident(incident_id):
    incident = Incident.query.get_or_404(incident_id)
    db.session.delete(incident)
    db.session.commit()
    flash('Произшествието е изтрито.', 'success')
    return redirect(url_for('incidents.list_incidents'))

@incidents_bp.route('/<int:incident_id>/resolve', methods=['GET', 'POST'])
@login_required
@staff_required
def resolve_incident(incident_id):
    incident = Incident.query.get_or_404(incident_id)
    
    if incident.is_resolved():
        flash('Това произшествие вече е разрешено.', 'warning')
        return redirect(url_for('incidents.detail_incident', incident_id=incident.id))
    
    if request.method == 'POST':
        lives_saved = request.form.get('lives_saved', 0)
        deaths = request.form.get('deaths', 0)
        outcome = request.form.get('outcome')
        resolution_notes = request.form.get('resolution_notes')
        injured = request.form.get('injured', 0)
        
        incident.lives_saved = int(lives_saved) if lives_saved else 0
        incident.deaths = int(deaths) if deaths else 0
        incident.outcome = outcome
        incident.resolution_notes = resolution_notes
        incident.status = 'resolved'
        incident.resolved_at = datetime.utcnow()
        incident.resolved_by_id = current_user.id
        
        db.session.commit()
        
        flash('Произшествието е разрешено успешно!', 'success')
        return redirect(url_for('incidents.detail_incident', incident_id=incident.id))
    
    return render_template('incidents/partials/resolve_modal.html', incident=incident)

@incidents_bp.route('/<int:incident_id>/mark-false', methods=['POST'])
@login_required
@role_required(['admin', 'incident_manager'])
def mark_false_alarm(incident_id):
    incident = Incident.query.get_or_404(incident_id)
    
    if incident.is_false_alarm:
        flash('Това произшествие вече е маркирано като фалшив сигнал.', 'warning')
        return redirect(url_for('incidents.detail_incident', incident_id=incident.id))
    
    incident.is_false_alarm = True
    incident.outcome = 'false_alarm'
    incident.status = 'resolved'
    incident.resolved_at = datetime.utcnow()
    incident.resolved_by_id = current_user.id
    incident.false_alarm_marked_by_id = current_user.id
    incident.false_alarm_marked_at = datetime.utcnow()
    
    warning = Warning(
        reason=f'Фалшив сигнал за произшествие #{incident.id} - "{incident.title}". Подаването на неверни сигнали е нарушение на Условията за ползване.',
        user_id=incident.created_by_id,
        issued_by_id=current_user.id
    )
    db.session.add(warning)
    
    db.session.commit()
    
    flash(f'Произшествието е маркирано като фалшив сигнал. Потребителят {incident.created_by.name} получи предупреждение.', 'success')
    return redirect(url_for('incidents.detail_incident', incident_id=incident.id))

@incidents_bp.route('/<int:incident_id>/assign-team', methods=['POST'])
@login_required
@role_required(['admin', 'incident_manager', 'dispatcher'])
def assign_team(incident_id):
    incident = Incident.query.get_or_404(incident_id)
    data = request.json
    team_id = data.get('team_id')
    
    if not team_id:
        return jsonify({'error': 'Team ID required'}), 400
    
    team = Team.query.get(team_id)
    if not team:
        return jsonify({'error': 'Team not found'}), 404
    
    if team.get_status() != 'available':
        return jsonify({'error': 'Team is not available'}), 400
    
    incident.assigned_team_id = team_id
    incident.status = 'active'
    incident.updated_at = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({'success': True, 'team_name': team.name})

@incidents_bp.route('/api/data')
@login_required
@staff_required
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
            'assigned_team': incident.assigned_team.name if incident.assigned_team else 'Не е назначен',
            'lives_saved': incident.lives_saved or 0,
            'deaths': incident.deaths or 0,
            'outcome': incident.get_outcome_display() if incident.outcome else '-',
            'is_false_alarm': incident.is_false_alarm
        })
    return jsonify(data)

@incidents_bp.route('/<int:incident_id>/update-status', methods=['POST'])
@login_required
@staff_required
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