from app import db
from datetime import datetime

class Resource(db.Model):
    __tablename__ = 'resources'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(50), nullable=False)  # vehicle, equipment, other
    quantity = db.Column(db.Integer, default=0)
    status = db.Column(db.String(50), default='available')  # available, in_use, low, depleted
    station_id = db.Column(db.Integer, nullable=True)  # 1, 2, 3 for Sofia, Plovdiv, Varna
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Resource {self.name}>'
    
    def get_category_display(self):
        category_map = {
            'vehicle': 'Превозно средство',
            'equipment': 'Оборудване',
            'other': 'Друго'
        }
        return category_map.get(self.category, self.category)
    
    def get_status_display(self):
        status_map = {
            'available': 'Наличен',
            'in_use': 'В употреба',
            'low': 'Ограничен',
            'depleted': 'Изчерпан'
        }
        return status_map.get(self.status, self.status)
    
    def get_unit(self):
        """Get unit based on category."""
        unit_map = {
            'vehicle': 'бр.',
            'equipment': 'бр.',
            'other': 'бр.'
        }
        return unit_map.get(self.category, 'бр.')