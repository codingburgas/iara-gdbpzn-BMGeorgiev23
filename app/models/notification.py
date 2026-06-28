from app import db
from datetime import datetime

class Notification(db.Model):
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(50), default='info')  # info, warning, success, danger
    is_read = db.Column(db.Boolean, default=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    incident_id = db.Column(db.Integer, db.ForeignKey('incidents.id'), nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='notifications')
    incident = db.relationship('Incident', backref='notifications')
    
    def __repr__(self):
        return f'<Notification {self.id}>'
    
    def get_type_display(self):
        type_map = {
            'info': 'Информация',
            'warning': 'Предупреждение',
            'success': 'Успех',
            'danger': 'Спешно'
        }
        return type_map.get(self.type, self.type)
    
    def get_time_display(self):
        return self.created_at.strftime('%d.%m.%Y %H:%M')