from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from . import auth_bp
from app import db
from app.models.user import User

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            if user.is_banned:
                flash(f'Вашият акаунт е блокиран. Причина: {user.ban_reason or "Не е посочена"}', 'danger')
                return render_template('auth/login.html')
            
            login_user(user)
            flash('Успешно влязохте.', 'success')
            next_page = request.args.get('next')
            
            # Redirect based on role
            if user.is_admin():
                return redirect(next_page or url_for('admin.users'))
            elif user.is_staff():
                return redirect(next_page or url_for('dashboard.index'))
            else:
                return redirect(next_page or url_for('main.user_dashboard'))
        else:
            flash('Невалиден имейл или парола', 'danger')
    
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        terms = request.form.get('terms')
        
        if not name or not email or not password:
            flash('Всички полета са задължителни.', 'danger')
            return render_template('auth/register.html')
        
        if password != confirm_password:
            flash('Паролите не съвпадат.', 'danger')
            return render_template('auth/register.html')
        
        if len(password) < 6:
            flash('Паролата трябва да бъде поне 6 символа.', 'danger')
            return render_template('auth/register.html')
        
        if not terms:
            flash('Моля, съгласете се с Условията за ползване.', 'danger')
            return render_template('auth/register.html')
        
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Този имейл вече е регистриран.', 'danger')
            return render_template('auth/register.html')
        
        hashed_password = generate_password_hash(password)
        user = User(
            name=name,
            email=email,
            password=hashed_password,
            role='user',
            is_active=True
        )
        
        db.session.add(user)
        db.session.commit()
        
        flash('Регистрацията е успешна! Можете да влезете.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Успешно излязохте от системата.', 'success')
    return redirect(url_for('auth.login'))