from app import db
from datetime import datetime

class Team(db.Model):
    __tablename__ = 'teams'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    
    # Station assignment
    station_id = db.Column(db.Integer, nullable=True)  # 1, 2, 3
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    members = db.relationship('User', back_populates='team', lazy=True)
    
    STATIONS = {
        1: 'Център',
        2: 'Люлин',
        3: 'Младост'
    }
    
    def get_station_display(self):
        return self.STATIONS.get(self.station_id, 'Не е назначена')
    
    def get_status(self):
        """Auto-calculate team status based on active incidents."""
        from app.models.incident import Incident
        active_incidents = Incident.query.filter(
            Incident.assigned_team_id == self.id,
            Incident.status.in_(['active', 'in_progress'])
        ).count()
        
        if active_incidents > 0:
            return 'on_mission'
        return 'available'
    
    def get_status_display(self):
        """Get human-readable status."""
        status = self.get_status()
        status_map = {
            'available': 'Наличен',
            'on_mission': 'На мисия'
        }
        return status_map.get(status, status)
    
    def get_status_badge_class(self):
        """Get Bootstrap badge class for status."""
        status = self.get_status()
        badge_map = {
            'available': 'bg-success',
            'on_mission': 'bg-warning text-dark'
        }
        return badge_map.get(status, 'bg-secondary')
    
    def __repr__(self):
        return f'<Team {self.name}>'