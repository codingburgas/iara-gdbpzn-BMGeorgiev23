from app import db
from datetime import datetime

class Team(db.Model):
    __tablename__ = 'teams'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), default='active')  # active, inactive, on_mission
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship - back_populates matches the property in User
    members = db.relationship('User', back_populates='team', lazy=True)
    
    def __repr__(self):
        return f'<Team {self.name}>'
    
    def get_status_display(self):
        status_map = {
            'active': 'Активен',
            'inactive': 'Неактивен',
            'on_mission': 'На мисия'
        }
        return status_map.get(self.status, self.status)