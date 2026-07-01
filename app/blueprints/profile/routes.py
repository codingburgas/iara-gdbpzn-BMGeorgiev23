from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
import os
from datetime import datetime  # <-- ADD THIS IMPORT
from . import profile_bp
from app import db
from app.models.user import User

@profile_bp.route('/')
@login_required
def index():
    return render_template('profile/index.html', title='Моят профил', user=current_user)

@profile_bp.route('/update', methods=['POST'])
@login_required
def update():
    user = current_user
    
    # Update basic info
    address = request.form.get('address')
    phone_number = request.form.get('phone_number')
    
    if address:
        user.address = address
    if phone_number:
        user.phone_number = phone_number
    
    db.session.commit()
    flash('Профилът беше обновен успешно.', 'success')
    return redirect(url_for('profile.index'))

@profile_bp.route('/change-password', methods=['POST'])
@login_required
def change_password():
    user = current_user
    
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')
    
    if not current_password or not new_password or not confirm_password:
        flash('Всички полета за парола са задължителни.', 'danger')
        return redirect(url_for('profile.index'))
    
    if not check_password_hash(user.password, current_password):
        flash('Текущата парола е неправилна.', 'danger')
        return redirect(url_for('profile.index'))
    
    if new_password != confirm_password:
        flash('Новите пароли не съвпадат.', 'danger')
        return redirect(url_for('profile.index'))
    
    if len(new_password) < 6:
        flash('Паролата трябва да бъде поне 6 символа.', 'danger')
        return redirect(url_for('profile.index'))
    
    user.set_password(new_password)
    db.session.commit()
    
    flash('Паролата беше променена успешно.', 'success')
    return redirect(url_for('profile.index'))

@profile_bp.route('/upload-picture', methods=['POST'])
@login_required
def upload_picture():
    user = current_user
    
    if 'profile_picture' not in request.files:
        flash('Не е избрана снимка.', 'danger')
        return redirect(url_for('profile.index'))
    
    file = request.files['profile_picture']
    if file.filename == '':
        flash('Не е избрана снимка.', 'danger')
        return redirect(url_for('profile.index'))
    
    if file:
        filename = secure_filename(file.filename)
        # Create unique filename
        ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        new_filename = f'profile_{user.id}_{datetime.utcnow().timestamp()}.{ext}'
        
        # Ensure upload directory exists
        upload_dir = os.path.join(current_app.root_path, 'static', 'uploads')
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        
        file_path = os.path.join(upload_dir, new_filename)
        file.save(file_path)
        
        # Update user
        user.profile_picture = new_filename
        db.session.commit()
        
        flash('Профилната снимка беше обновена успешно.', 'success')
    
    return redirect(url_for('profile.index'))