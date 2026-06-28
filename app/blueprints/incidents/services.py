from app import db
from app.models.incident import Incident

class IncidentService:
    @staticmethod
    def create_incident(data):
        incident = Incident(**data)
        db.session.add(incident)
        db.session.commit()
        return incident
    
    @staticmethod
    def get_incident(incident_id):
        return Incident.query.get(incident_id)
    
    @staticmethod
    def get_all_incidents():
        return Incident.query.all()