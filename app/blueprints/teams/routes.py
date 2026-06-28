from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from . import teams_bp
from app import db
from app.models.team import Team
from app.models.user import User

@teams_bp.route('/')
@login_required
def list_teams():
    teams = Team.query.order_by(Team.name).all()
    return render_template('teams/list.html', title='Екипи', teams=teams)

@teams_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_team():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        status = request.form.get('status', 'active')
        
        if not name:
            flash('Името на екипа е задължително.', 'danger')
            return render_template('teams/create.html')
        
        existing = Team.query.filter_by(name=name).first()
        if existing:
            flash('Екип с това име вече съществува.', 'danger')
            return render_template('teams/create.html')
        
        team = Team(
            name=name,
            description=description,
            status=status
        )
        
        db.session.add(team)
        db.session.commit()
        
        flash('Екипът е създаден успешно.', 'success')
        return redirect(url_for('teams.list_teams'))
    
    return render_template('teams/create.html')

@teams_bp.route('/<int:team_id>')
@login_required
def detail_team(team_id):
    team = Team.query.get_or_404(team_id)
    members = User.query.filter_by(team_id=team.id).all()
    return render_template('teams/detail.html', title='Детайли на екип', team=team, members=members)

@teams_bp.route('/<int:team_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_team(team_id):
    team = Team.query.get_or_404(team_id)
    
    if request.method == 'POST':
        team.name = request.form.get('name')
        team.description = request.form.get('description')
        team.status = request.form.get('status')
        team.updated_at = datetime.utcnow()
        
        db.session.commit()
        flash('Екипът е обновен успешно.', 'success')
        return redirect(url_for('teams.detail_team', team_id=team.id))
    
    return render_template('teams/edit.html', title='Редактиране на екип', team=team)

@teams_bp.route('/<int:team_id>/delete', methods=['POST'])
@login_required
def delete_team(team_id):
    team = Team.query.get_or_404(team_id)
    
    # Check if team has members
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
def add_member(team_id):
    team = Team.query.get_or_404(team_id)
    user_id = request.form.get('user_id')
    
    if not user_id:
        flash('Моля, изберете служител.', 'danger')
        return redirect(url_for('teams.detail_team', team_id=team.id))
    
    user = User.query.get_or_404(user_id)
    
    if user.team_id:
        flash(f'{user.name} вече е в друг екип.', 'danger')
        return redirect(url_for('teams.detail_team', team_id=team.id))
    
    user.team_id = team.id
    db.session.commit()
    
    flash(f'{user.name} беше добавен към екипа.', 'success')
    return redirect(url_for('teams.detail_team', team_id=team.id))

@teams_bp.route('/<int:team_id>/remove-member/<int:user_id>', methods=['POST'])
@login_required
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