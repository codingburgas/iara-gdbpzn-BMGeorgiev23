from app import db
from datetime import datetime

class Channel(db.Model):
    __tablename__ = 'channels'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    channel_type = db.Column(db.String(50), default='general')  # general, team
    
    # For team channels
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=True)
    
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    created_by = db.relationship('User', backref='created_channels')
    team = db.relationship('Team', backref='channels')
    messages = db.relationship('Message', back_populates='channel', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Channel {self.name}>'
    
    def get_type_display(self):
        type_map = {
            'general': 'Общ',
            'team': 'Екип'
        }
        return type_map.get(self.channel_type, self.channel_type)
    
    def can_user_access(self, user):
        """Check if a user has access to this channel."""
        if user.is_admin() or user.is_incident_manager():
            return True
        if self.channel_type == 'general':
            return user.is_staff()
        if self.channel_type == 'team' and self.team_id:
            return user.team_id == self.team_id
        return False