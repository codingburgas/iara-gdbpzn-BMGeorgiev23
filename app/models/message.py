from app import db
from datetime import datetime

class Message(db.Model):
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    is_template = db.Column(db.Boolean, default=False)
    template_name = db.Column(db.String(100), nullable=True)
    is_emergency = db.Column(db.Boolean, default=False)  # NEW FIELD
    
    incident_id = db.Column(db.Integer, db.ForeignKey('incidents.id'), nullable=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    incident = db.relationship('Incident', backref='messages')
    sender = db.relationship('User', backref='sent_messages')
    
    def __repr__(self):
        return f'<Message {self.id}>'
    
    def get_time_display(self):
        return self.created_at.strftime('%d.%m.%Y %H:%M')