from functools import wraps
from flask import flash, redirect, url_for, abort
from flask_login import current_user

def role_required(roles):
    """
    Decorator to restrict access to specific roles.
    Usage: @role_required(['admin']) or @role_required(['admin', 'firefighter'])
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Моля, влезте в системата.', 'warning')
                return redirect(url_for('auth.login'))
            
            if current_user.is_banned:
                flash(f'Вашият акаунт е блокиран. Причина: {current_user.ban_reason or "Не е посочена"}', 'danger')
                return redirect(url_for('main.index'))
            
            if current_user.role not in roles:
                flash('Нямате достъп до тази страница.', 'danger')
                return abort(403)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    """Decorator for admin-only access."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Моля, влезте в системата.', 'warning')
            return redirect(url_for('auth.login'))
        
        if current_user.is_banned:
            flash(f'Вашият акаунт е блокиран. Причина: {current_user.ban_reason or "Не е посочена"}', 'danger')
            return redirect(url_for('main.index'))
        
        if not current_user.is_admin():
            flash('Само администратори имат достъп до тази страница.', 'danger')
            return abort(403)
        
        return f(*args, **kwargs)
    return decorated_function

def staff_required(f):
    """Decorator for any staff member (admin, incident_manager, dispatcher, firefighter)."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Моля, влезте в системата.', 'warning')
            return redirect(url_for('auth.login'))
        
        if current_user.is_banned:
            flash(f'Вашият акаунт е блокиран. Причина: {current_user.ban_reason or "Не е посочена"}', 'danger')
            return redirect(url_for('main.index'))
        
        if not current_user.is_staff():
            flash('Нямате достъп до тази страница.', 'danger')
            return abort(403)
        
        return f(*args, **kwargs)
    return decorated_function

def firefighter_required(f):
    """Decorator for firefighter access (includes all staff)."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Моля, влезте в системата.', 'warning')
            return redirect(url_for('auth.login'))
        
        if current_user.is_banned:
            flash(f'Вашият акаунт е блокиран. Причина: {current_user.ban_reason or "Не е посочена"}', 'danger')
            return redirect(url_for('main.index'))
        
        if not current_user.is_staff():
            flash('Само служители имат достъп до тази страница.', 'danger')
            return abort(403)
        
        return f(*args, **kwargs)
    return decorated_function

def permission_required(permission):
    """
    Decorator to check if user has a specific permission.
    Usage: @permission_required('incident_resolve')
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Моля, влезте в системата.', 'warning')
                return redirect(url_for('auth.login'))
            
            if current_user.is_banned:
                flash(f'Вашият акаунт е блокиран. Причина: {current_user.ban_reason or "Не е посочена"}', 'danger')
                return redirect(url_for('main.index'))
            
            if not current_user.has_permission(permission):
                flash('Нямате необходимите права за това действие.', 'danger')
                return abort(403)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def check_ban(f):
    """Decorator to check if user is banned."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated and current_user.is_banned:
            flash(f'Вашият акаунт е блокиран. Причина: {current_user.ban_reason or "Не е посочена"}', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function