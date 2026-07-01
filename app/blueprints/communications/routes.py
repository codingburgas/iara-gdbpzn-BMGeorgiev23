from flask import render_template, request, jsonify, session, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime
from . import communications_bp
from app import db
from app.models.message import Message
from app.models.notification import Notification
from app.models.incident import Incident
from app.models.user import User
from app.models.channel import Channel
from app.models.team import Team
from app.utils.decorators import staff_required, admin_required

@communications_bp.route('/')
@login_required
@staff_required
def chat():
    incidents = Incident.query.filter(Incident.status.in_(['active', 'in_progress'])).all()
    channels = Channel.query.all()
    teams = Team.query.all()
    return render_template('communications/chat.html', title='Чат', incidents=incidents, channels=channels, teams=teams)

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

# API Routes
@communications_bp.route('/api/messages', methods=['GET', 'POST'])
@login_required
@staff_required
def api_messages():
    if request.method == 'GET':
        incident_id = request.args.get('incident_id')
        channel_id = request.args.get('channel_id')
        query = Message.query.filter_by(is_template=False)
        
        if incident_id:
            query = query.filter_by(incident_id=incident_id)
        elif channel_id:
            channel = Channel.query.get(channel_id)
            if channel and not channel.can_user_access(current_user):
                return jsonify({'error': 'Access denied'}), 403
            query = query.filter_by(channel_id=channel_id)
        else:
            query = query.filter_by(incident_id=None, channel_id=None)
        
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
        incident_id = data.get('incident_id')
        channel_id = data.get('channel_id')
        
        if channel_id:
            channel = Channel.query.get(channel_id)
            if channel and not channel.can_user_access(current_user):
                return jsonify({'error': 'Access denied'}), 403
        
        message = Message(
            content=data.get('content'),
            incident_id=incident_id if incident_id else None,
            channel_id=channel_id if channel_id else None,
            sender_id=current_user.id,
            is_template=False,
            is_emergency=data.get('is_emergency', False)
        )
        db.session.add(message)
        db.session.commit()
        return jsonify({'success': True, 'id': message.id})

@communications_bp.route('/api/channels', methods=['GET', 'POST'])
@login_required
@staff_required
def api_channels():
    if request.method == 'GET':
        channels = Channel.query.all()
        return jsonify([{
            'id': c.id,
            'name': c.name,
            'description': c.description,
            'type': c.channel_type,
            'type_display': c.get_type_display(),
            'team_id': c.team_id,
            'team_name': c.team.name if c.team else None,
            'created_by': c.created_by.name,
            'created_at': c.created_at.strftime('%d.%m.%Y %H:%M'),
            'access_info': 'Всички служители' if c.channel_type == 'general' else f'Екип "{c.team.name}"' if c.team else 'Ограничен'
        } for c in channels])
    
    elif request.method == 'POST':
        data = request.json
        channel = Channel(
            name=data.get('name'),
            description=data.get('description'),
            channel_type=data.get('channel_type', 'general'),
            team_id=data.get('team_id') if data.get('channel_type') == 'team' else None,
            created_by_id=current_user.id
        )
        db.session.add(channel)
        db.session.commit()
        return jsonify({'success': True, 'id': channel.id, 'name': channel.name})

@communications_bp.route('/api/channels/<int:channel_id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def api_channel_detail(channel_id):
    channel = Channel.query.get_or_404(channel_id)
    
    if request.method == 'GET':
        return jsonify({
            'id': channel.id,
            'name': channel.name,
            'description': channel.description,
            'type': channel.channel_type,
            'type_display': channel.get_type_display(),
            'team_id': channel.team_id,
            'team_name': channel.team.name if channel.team else None,
            'created_by': channel.created_by.name,
            'created_at': channel.created_at.strftime('%d.%m.%Y %H:%M'),
            'access_info': 'Всички служители' if channel.channel_type == 'general' else f'Екип "{channel.team.name}"' if channel.team else 'Ограничен'
        })
    
    elif request.method == 'PUT':
        if not current_user.is_admin():
            return jsonify({'error': 'Unauthorized'}), 403
        
        data = request.json
        channel.name = data.get('name', channel.name)
        channel.channel_type = data.get('channel_type', channel.channel_type)
        
        if channel.channel_type == 'team':
            channel.team_id = data.get('team_id')
        else:
            channel.team_id = None
        
        db.session.commit()
        return jsonify({'success': True, 'id': channel.id})
    
    elif request.method == 'DELETE':
        if not current_user.is_admin():
            return jsonify({'error': 'Unauthorized'}), 403
        
        db.session.delete(channel)
        db.session.commit()
        return jsonify({'success': True})

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