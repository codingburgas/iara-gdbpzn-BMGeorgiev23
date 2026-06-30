from flask import render_template, request, jsonify, session, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime
from . import communications_bp
from app import db
from app.models.message import Message
from app.models.notification import Notification
from app.models.incident import Incident
from app.models.user import User
from app.utils.decorators import staff_required

@communications_bp.route('/')
@login_required
@staff_required
def chat():
    # Only show active and in_progress incidents (exclude resolved/closed)
    incidents = Incident.query.filter(Incident.status.in_(['active', 'in_progress'])).all()
    templates = Message.query.filter_by(is_template=True).all()
    return render_template('communications/chat.html', title='Чат', incidents=incidents, templates=templates)

@communications_bp.route('/video')
@login_required
@staff_required
def video_call():
    return render_template('communications/video_call.html', title='Видео обаждане')

@communications_bp.route('/notifications')
@login_required
def notifications():
    notifications = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.created_at.desc()).all()
    unread_count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
    return render_template('communications/notifications.html', title='Известия', notifications=notifications, unread_count=unread_count)

@communications_bp.route('/templates')
@login_required
@staff_required
def message_templates():
    templates = Message.query.query.filter_by(is_template=True).all()
    return render_template('communications/message_templates.html', title='Шаблони за съобщения', templates=templates)

# API Routes (keep as is, with staff_required where needed)
@communications_bp.route('/api/messages', methods=['GET', 'POST'])
@login_required
@staff_required
def api_messages():
    if request.method == 'GET':
        incident_id = request.args.get('incident_id')
        query = Message.query.filter_by(is_template=False)
        if incident_id:
            query = query.filter_by(incident_id=incident_id)
        messages = query.order_by(Message.created_at.asc()).all()
        return jsonify([{
            'id': m.id,
            'content': m.content,
            'sender': m.sender.name,
            'created_at': m.get_time_display(),
            'is_emergency': getattr(m, 'is_emergency', False)
        } for m in messages])
    
    elif request.method == 'POST':
        data = request.json
        message = Message(
            content=data.get('content'),
            incident_id=data.get('incident_id'),
            sender_id=current_user.id,
            is_template=False,
            is_emergency=data.get('is_emergency', False)
        )
        db.session.add(message)
        db.session.commit()
        return jsonify({'success': True, 'id': message.id})

@communications_bp.route('/api/notifications/<int:notification_id>/read', methods=['POST'])
@login_required
def mark_notification_read(notification_id):
    notification = Notification.query.get_or_404(notification_id)
    if notification.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    notification.is_read = True
    db.session.commit()
    return jsonify({'success': True})

@communications_bp.route('/api/notifications/mark-all-read', methods=['POST'])
@login_required
def mark_all_read():
    Notification.query.filter_by(user_id=current_user.id, is_read=False).update({'is_read': True})
    db.session.commit()
    return jsonify({'success': True})

@communications_bp.route('/api/templates', methods=['GET', 'POST'])
@login_required
@staff_required
def api_templates():
    if request.method == 'GET':
        templates = Message.query.filter_by(is_template=True).all()
        return jsonify([{
            'id': t.id,
            'name': t.template_name,
            'content': t.content
        } for t in templates])
    
    elif request.method == 'POST':
        data = request.json
        template = Message(
            content=data.get('content'),
            is_template=True,
            template_name=data.get('name'),
            sender_id=current_user.id
        )
        db.session.add(template)
        db.session.commit()
        return jsonify({'success': True, 'id': template.id})

@communications_bp.route('/api/notifications/create', methods=['POST'])
@login_required
@staff_required
def create_notification():
    data = request.json
    notification = Notification(
        title=data.get('title'),
        message=data.get('message'),
        type=data.get('type', 'info'),
        user_id=data.get('user_id'),
        incident_id=data.get('incident_id')
    )
    db.session.add(notification)
    db.session.commit()
    return jsonify({'success': True, 'id': notification.id})

@communications_bp.route('/api/notifications/unread-count')
@login_required
def unread_count():
    count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
    return jsonify({'count': count})