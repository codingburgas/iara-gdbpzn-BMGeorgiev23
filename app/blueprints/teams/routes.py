from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from . import teams_bp
from app import db
from app.models.team import Team
from app.models.user import User
from app.models.incident import Incident
from app.utils.decorators import staff_required, admin_required

@teams_bp.route('/')
@login_required
@staff_required
def list_teams():
    teams = Team.query.order_by(Team.name).all()
    return render_template('teams/list.html', title='Екипи', teams=teams)

@teams_bp.route('/create', methods=['GET', 'POST'])
@login_required
@staff_required
def create_team():
    # Get all firefighters (users with role 'firefighter')
    available_members = User.query.filter(
        User.role == 'firefighter',
        User.team_id.is_(None),
        User.is_active == True
    ).all()
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        member_ids = request.form.getlist('members')
        
        if not name:
            flash('Името на екипа е задължително.', 'danger')
            return render_template('teams/create.html', available_members=available_members)
        
        existing = Team.query.filter_by(name=name).first()
        if existing:
            flash('Екип с това име вече съществува.', 'danger')
            return render_template('teams/create.html', available_members=available_members)
        
        team = Team(
            name=name,
            description=description
        )
        
        db.session.add(team)
        db.session.flush()
        
        if member_ids:
            members = User.query.filter(User.id.in_(member_ids)).all()
            for member in members:
                member.team_id = team.id
        
        db.session.commit()
        
        flash('Екипът е създаден успешно.', 'success')
        return redirect(url_for('teams.list_teams'))
    
    return render_template('teams/create.html', available_members=available_members)

@teams_bp.route('/<int:team_id>')
@login_required
@staff_required
def detail_team(team_id):
    team = Team.query.get_or_404(team_id)
    members = User.query.filter_by(team_id=team.id).all()
    active_incidents = Incident.query.filter(
        Incident.assigned_team_id == team.id,
        Incident.status.in_(['active', 'in_progress'])
    ).all()
    users = User.query.filter(
        User.is_active == True
    ).all()
    return render_template('teams/detail.html', title='Детайли на екип', team=team, members=members, active_incidents=active_incidents, users=users)

@teams_bp.route('/<int:team_id>/edit', methods=['GET', 'POST'])
@login_required
@staff_required
def edit_team(team_id):
    team = Team.query.get_or_404(team_id)
    
    # Get all firefighters (users with role 'firefighter')
    all_firefighters = User.query.filter(
        User.role == 'firefighter',
        User.is_active == True
    ).all()
    
    current_members = User.query.filter_by(team_id=team.id).all()
    current_member_ids = [m.id for m in current_members]
    
    if request.method == 'POST':
        team.name = request.form.get('name')
        team.description = request.form.get('description')
        team.updated_at = datetime.utcnow()
        
        member_ids = request.form.getlist('members')
        
        for member in current_members:
            member.team_id = None
        
        if member_ids:
            new_members = User.query.filter(User.id.in_(member_ids)).all()
            for member in new_members:
                member.team_id = team.id
        
        db.session.commit()
        flash('Екипът е обновен успешно.', 'success')
        return redirect(url_for('teams.detail_team', team_id=team.id))
    
    return render_template(
        'teams/edit.html',
        title='Редактиране на екип',
        team=team,
        all_firefighters=all_firefighters,
        current_member_ids=current_member_ids
    )

@teams_bp.route('/<int:team_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_team(team_id):
    team = Team.query.get_or_404(team_id)
    
    members = User.query.filter_by(team_id=team.id).count()
    if members > 0:
        flash('Не можете да изтриете екип с назначени членове.', 'danger')
        return redirect(url_for('teams.detail_team', team_id=team.id))
    
    db.session.delete(team)
    db.session.commit()
    flash('Екипът е изтрит успешно.', 'success')
    return redirect(url_for('teams.list_teams'))

@teams_bp.route('/<int:team_id>/add-member', methods=['POST'])
@login_required
@staff_required
def add_member(team_id):
    team = Team.query.get_or_404(team_id)
    user_id = request.form.get('user_id')
    
    if not user_id:
        flash('Моля, изберете служител.', 'danger')
        return redirect(url_for('teams.detail_team', team_id=team.id))
    
    user = User.query.get_or_404(user_id)
    
    if user.role != 'firefighter':
        flash('Можете да добавяте само пожарникари.', 'danger')
        return redirect(url_for('teams.detail_team', team_id=team.id))
    
    if user.team_id:
        flash(f'{user.name} вече е в друг екип.', 'danger')
        return redirect(url_for('teams.detail_team', team_id=team.id))
    
    user.team_id = team.id
    db.session.commit()
    
    flash(f'{user.name} беше добавен към екипа.', 'success')
    return redirect(url_for('teams.detail_team', team_id=team.id))

@teams_bp.route('/<int:team_id>/remove-member/<int:user_id>', methods=['POST'])
@login_required
@staff_required
def remove_member(team_id, user_id):
    team = Team.query.get_or_404(team_id)
    user = User.query.get_or_404(user_id)
    
    if user.team_id != team.id:
        flash('Този служител не е в този екип.', 'danger')
        return redirect(url_for('teams.detail_team', team_id=team.id))
    
    user.team_id = None
    db.session.commit()
    
    flash(f'{user.name} беше премахнат от екипа.', 'success')
    return redirect(url_for('teams.detail_team', team_id=team.id))

@teams_bp.route('/api/data')
@login_required
@staff_required
def api_teams_data():
    teams = Team.query.all()
    data = []
    for team in teams:
        member_count = User.query.filter_by(team_id=team.id).count()
        data.append({
            'id': team.id,
            'name': team.name,
            'status': team.get_status_display(),
            'members': member_count,
            'created_at': team.created_at.strftime('%Y-%m-%d %H:%M')
        })
    return jsonify(data)