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
    
    # Role: admin, incident_manager, dispatcher, firefighter, user
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
    
    # Warnings relationship
    warnings = db.relationship('Warning', foreign_keys='Warning.user_id', backref='user', lazy=True, cascade='all, delete-orphan')
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Role definitions
    ROLES = {
        'admin': 'Администратор',
        'incident_manager': 'Мениджър произшествия',
        'dispatcher': 'Диспечер',
        'firefighter': 'Пожарникар',
        'user': 'Потребител'
    }
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def get_role_display(self):
        return self.ROLES.get(self.role, self.role)
    
    def is_admin(self):
        return self.role == 'admin'
    
    def is_incident_manager(self):
        return self.role == 'incident_manager'
    
    def is_dispatcher(self):
        return self.role == 'dispatcher'
    
    def is_firefighter(self):
        return self.role == 'firefighter'
    
    def is_regular_user(self):
        return self.role == 'user'
    
    def is_staff(self):
        """Check if user is any staff role (not a regular user)"""
        return self.role in ['admin', 'incident_manager', 'dispatcher', 'firefighter']
    
    def has_permission(self, permission):
        """Check if user has a specific permission"""
        from app.utils.permissions import has_permission
        return has_permission(self, permission)
    
    def __repr__(self):
        return f'<User {self.email}>'