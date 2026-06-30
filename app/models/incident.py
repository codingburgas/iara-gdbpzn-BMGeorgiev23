from app import db
from datetime import datetime

class Incident(db.Model):
    __tablename__ = 'incidents'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    type = db.Column(db.String(50), nullable=False)  # fire, rescue, other
    status = db.Column(db.String(50), default='active')  # active, in_progress, resolved, closed
    priority = db.Column(db.String(20), default='medium')  # critical, high, medium, low
    
    address = db.Column(db.String(300), nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    
    # Resolution fields
    lives_saved = db.Column(db.Integer, default=0)
    deaths = db.Column(db.Integer, default=0)
    outcome = db.Column(db.String(50), nullable=True)  # success, partial, failure
    resolution_notes = db.Column(db.Text, nullable=True)
    resolved_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    resolved_at = db.Column(db.DateTime, nullable=True)
    
    # Foreign keys
    assigned_team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=True)
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    assigned_team = db.relationship('Team', backref='incidents')
    created_by = db.relationship('User', foreign_keys=[created_by_id], backref='created_incidents')
    resolved_by = db.relationship('User', foreign_keys=[resolved_by_id], backref='resolved_incidents')
    
    def __repr__(self):
        return f'<Incident {self.title}>'
    
    def get_status_display(self):
        status_map = {
            'active': 'Активен',
            'in_progress': 'В процес',
            'resolved': 'Разрешен',
            'closed': 'Затворен'
        }
        return status_map.get(self.status, self.status)
    
    def get_priority_display(self):
        priority_map = {
            'critical': 'Критичен',
            'high': 'Висок',
            'medium': 'Среден',
            'low': 'Нисък'
        }
        return priority_map.get(self.priority, self.priority)
    
    def get_type_display(self):
        type_map = {
            'fire': 'Пожар',
            'rescue': 'Спасителна операция',
            'other': 'Друго'
        }
        return type_map.get(self.type, self.type)
    
    def get_outcome_display(self):
        outcome_map = {
            'success': 'Успешен',
            'partial': 'Частичен успех',
            'failure': 'Неуспешен'
        }
        return outcome_map.get(self.outcome, self.outcome)
    
    def is_resolved(self):
        return self.status in ['resolved', 'closed']