from app import db
from datetime import datetime

class Warning(db.Model):
    __tablename__ = 'warnings'
    
    id = db.Column(db.Integer, primary_key=True)
    reason = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    issued_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Specify foreign_keys to resolve ambiguity
    issued_by = db.relationship('User', foreign_keys=[issued_by_id], backref='issued_warnings')
    
    def __repr__(self):
        return f'<Warning {self.id} for User {self.user_id}>'
    
    def get_time_display(self):
        return self.created_at.strftime('%d.%m.%Y %H:%M')