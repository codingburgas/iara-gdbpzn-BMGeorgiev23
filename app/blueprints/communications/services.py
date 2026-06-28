from app import db
from app.models.message import Message
from app.models.notification import Notification
from app.models.user import User
from datetime import datetime

class CommunicationService:
    
    @staticmethod
    def send_message(content, incident_id, sender_id):
        message = Message(
            content=content,
            incident_id=incident_id,
            sender_id=sender_id
        )
        db.session.add(message)
        db.session.commit()
        return message
    
    @staticmethod
    def send_notification(title, message, user_id, type='info', incident_id=None):
        notification = Notification(
            title=title,
            message=message,
            type=type,
            user_id=user_id,
            incident_id=incident_id
        )
        db.session.add(notification)
        db.session.commit()
        return notification
    
    @staticmethod
    def send_bulk_notification(title, message, user_ids, type='info', incident_id=None):
        notifications = []
        for user_id in user_ids:
            notification = Notification(
                title=title,
                message=message,
                type=type,
                user_id=user_id,
                incident_id=incident_id
            )
            notifications.append(notification)
        db.session.add_all(notifications)
        db.session.commit()
        return notifications
    
    @staticmethod
    def get_unread_count(user_id):
        return Notification.query.filter_by(user_id=user_id, is_read=False).count()
    
    @staticmethod
    def get_templates():
        return Message.query.filter_by(is_template=True).all()
    
    @staticmethod
    def create_template(name, content, created_by):
        template = Message(
            content=content,
            is_template=True,
            template_name=name,
            sender_id=created_by
        )
        db.session.add(template)
        db.session.commit()
        return template