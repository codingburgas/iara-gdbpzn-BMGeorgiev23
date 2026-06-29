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

def firefighter_required(f):
    """Decorator for firefighter-only access (includes admins)."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Моля, влезте в системата.', 'warning')
            return redirect(url_for('auth.login'))
        
        if current_user.is_banned:
            flash(f'Вашият акаунт е блокиран. Причина: {current_user.ban_reason or "Не е посочена"}', 'danger')
            return redirect(url_for('main.index'))
        
        if not current_user.is_firefighter():
            flash('Само пожарникари и администратори имат достъп до тази страница.', 'danger')
            return abort(403)
        
        return f(*args, **kwargs)
    return decorated_function

def check_ban(f):
    """Decorator to check if user is banned."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated and current_user.is_banned:
            flash(f'Вашият акаунт е блокиран. Причина: {current_user.ban_reason or "Не е посочена"}', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function