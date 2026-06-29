from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    
    # Role: admin, firefighter, user
    role = db.Column(db.String(50), default='user')
    
    # Ban fields
    is_banned = db.Column(db.Boolean, default=False)
    ban_reason = db.Column(db.Text, nullable=True)
    banned_at = db.Column(db.DateTime, nullable=True)
    banned_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # Foreign key to Team
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=True)
    
    # Relationships
    team = db.relationship('Team', back_populates='members', foreign_keys=[team_id])
    banned_by = db.relationship('User', remote_side=[id], foreign_keys=[banned_by_id])
    
    # Warnings relationship - specify foreign_keys to resolve ambiguity
    warnings = db.relationship('Warning', foreign_keys='Warning.user_id', backref='user', lazy=True, cascade='all, delete-orphan')
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def get_role_display(self):
        role_map = {
            'admin': 'Администратор',
            'firefighter': 'Пожарникар',
            'user': 'Потребител'
        }
        return role_map.get(self.role, self.role)
    
    def is_admin(self):
        return self.role == 'admin'
    
    def is_firefighter(self):
        return self.role == 'firefighter' or self.role == 'admin'
    
    def is_regular_user(self):
        return self.role == 'user'
    
    def has_access_to(self, feature):
        access_map = {
            'dashboard': ['admin', 'firefighter'],
            'incidents_view': ['admin', 'firefighter'],
            'incidents_edit': ['admin', 'firefighter'],
            'incidents_delete': ['admin'],
            'teams': ['admin', 'firefighter'],
            'operations': ['admin', 'firefighter'],
            'communications': ['admin', 'firefighter'],
            'resources': ['admin', 'firefighter'],
            'reports': ['admin', 'firefighter'],
            'user_management': ['admin']
        }
        return self.role in access_map.get(feature, [])
    
    def __repr__(self):
        return f'<User {self.email}>'