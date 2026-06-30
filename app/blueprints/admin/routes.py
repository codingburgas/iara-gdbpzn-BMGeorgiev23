from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from . import admin_bp
from app import db
from app.models.user import User
from app.models.warning import Warning
from app.utils.decorators import admin_required

@admin_bp.route('/')
@login_required
@admin_required
def index():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', title='Управление на потребители', users=users)

@admin_bp.route('/users')
@login_required
@admin_required
def users():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', title='Потребители', users=users)

@admin_bp.route('/user/<int:user_id>')
@login_required
@admin_required
def user_detail(user_id):
    user = User.query.get_or_404(user_id)
    warnings = Warning.query.filter_by(user_id=user.id).order_by(Warning.created_at.desc()).all()
    return render_template('admin/user_detail.html', title='Детайли на потребител', user=user, warnings=warnings)

@admin_bp.route('/user/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def user_edit(user_id):
    user = User.query.get_or_404(user_id)
    
    if user.id == current_user.id:
        flash('Не можете да редактирате собствения си профил тук.', 'warning')
        return redirect(url_for('admin.user_detail', user_id=user.id))
    
    if request.method == 'POST':
        user.name = request.form.get('name')
        user.email = request.form.get('email')
        user.role = request.form.get('role')
        user.is_active = 'is_active' in request.form
        
        if request.form.get('password'):
            user.set_password(request.form.get('password'))
        
        db.session.commit()
        flash('Потребителят е обновен успешно.', 'success')
        return redirect(url_for('admin.user_detail', user_id=user.id))
    
    return render_template('admin/user_edit.html', title='Редактиране на потребител', user=user)

@admin_bp.route('/user/<int:user_id>/ban', methods=['POST'])
@login_required
@admin_required
def ban_user(user_id):
    user = User.query.get_or_404(user_id)
    
    if user.id == current_user.id:
        flash('Не можете да блокирате себе си.', 'danger')
        return redirect(url_for('admin.user_detail', user_id=user.id))
    
    if user.is_admin():
        flash('Не можете да блокирате администратор.', 'danger')
        return redirect(url_for('admin.user_detail', user_id=user.id))
    
    reason = request.form.get('reason', 'Не е посочена причина')
    
    user.is_banned = True
    user.ban_reason = reason
    user.banned_at = datetime.utcnow()
    user.banned_by_id = current_user.id
    
    db.session.commit()
    flash(f'Потребителят {user.name} беше блокиран.', 'success')
    return redirect(url_for('admin.user_detail', user_id=user.id))

@admin_bp.route('/user/<int:user_id>/unban', methods=['POST'])
@login_required
@admin_required
def unban_user(user_id):
    user = User.query.get_or_404(user_id)
    
    user.is_banned = False
    user.ban_reason = None
    user.banned_at = None
    user.banned_by_id = None
    
    db.session.commit()
    flash(f'Потребителят {user.name} беше разблокиран.', 'success')
    return redirect(url_for('admin.user_detail', user_id=user.id))

@admin_bp.route('/user/<int:user_id>/warning', methods=['POST'])
@login_required
@admin_required
def add_warning(user_id):
    user = User.query.get_or_404(user_id)
    reason = request.form.get('reason')
    
    if not reason:
        flash('Моля, въведете причина за предупреждението.', 'danger')
        return redirect(url_for('admin.user_detail', user_id=user.id))
    
    warning = Warning(
        reason=reason,
        user_id=user.id,
        issued_by_id=current_user.id
    )
    
    db.session.add(warning)
    db.session.commit()
    
    flash(f'Предупреждение добавено за {user.name}.', 'success')
    return redirect(url_for('admin.user_detail', user_id=user.id))

@admin_bp.route('/user/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    
    if user.id == current_user.id:
        flash('Не можете да изтриете себе си.', 'danger')
        return redirect(url_for('admin.users'))
    
    if user.is_admin():
        flash('Не можете да изтриете администратор.', 'danger')
        return redirect(url_for('admin.users'))
    
    db.session.delete(user)
    db.session.commit()
    
    flash(f'Потребителят {user.name} беше изтрит.', 'success')
    return redirect(url_for('admin.users'))

@admin_bp.route('/create-admin', methods=['GET', 'POST'])
@login_required
@admin_required
def create_admin():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        
        if User.query.filter_by(email=email).first():
            flash('Този имейл вече е регистриран.', 'danger')
            return render_template('admin/create_admin.html')
        
        user = User(
            email=email,
            name=name,
            role='admin',
            is_active=True
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Нов администратор създаден успешно.', 'success')
        return redirect(url_for('admin.users'))
    
    return render_template('admin/create_admin.html')

@admin_bp.route('/create-user', methods=['GET', 'POST'])
@login_required
@admin_required
def create_user():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        role = request.form.get('role', 'user')
        
        if User.query.filter_by(email=email).first():
            flash('Този имейл вече е регистриран.', 'danger')
            return render_template('admin/create_user.html')
        
        user = User(
            email=email,
            name=name,
            role=role,
            is_active=True
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash(f'Потребителят е създаден успешно с роля: {user.get_role_display()}.', 'success')
        return redirect(url_for('admin.users'))
    
    return render_template('admin/create_user.html')