from flask import render_template, jsonify, request
from flask_login import login_required
from datetime import datetime
from math import radians, sin, cos, sqrt, atan2
from . import operations_bp
from app import db
from app.models.incident import Incident
from app.models.team import Team
from app.models.user import User
from app.models.resource import Resource
from app.utils.decorators import staff_required, role_required

# Station coordinates (Sofia locations)
STATION_COORDS = {
    1: {'lat': 42.6977, 'lng': 23.3219, 'name': 'Център'},
    2: {'lat': 42.7200, 'lng': 23.2800, 'name': 'Люлин'},
    3: {'lat': 42.6500, 'lng': 23.3800, 'name': 'Младост'}
}

def haversine(lat1, lon1, lat2, lon2):
    """Calculate the great circle distance between two points in kilometers."""
    R = 6371  # Earth's radius in kilometers
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c

def find_nearest_station(lat, lng):
    """Find the nearest station to a given location."""
    nearest = None
    min_distance = float('inf')
    for station_id, coords in STATION_COORDS.items():
        dist = haversine(lat, lng, coords['lat'], coords['lng'])
        if dist < min_distance:
            min_distance = dist
            nearest = station_id
    return nearest

@operations_bp.route('/')
@login_required
@staff_required
def live():
    # Get all incidents
    all_incidents = Incident.query.all()
    
    # For each incident, calculate nearest station if not already set
    for incident in all_incidents:
        if incident.latitude and incident.longitude and not incident.nearest_station_id:
            incident.nearest_station_id = find_nearest_station(incident.latitude, incident.longitude)
            db.session.commit()
    
    # Split into awaiting and active
    awaiting_incidents = [i for i in all_incidents if i.status == 'awaiting_assignment']
    active_incidents = [i for i in all_incidents if i.status in ['active', 'in_progress']]
    
    # Get all teams
    all_teams = Team.query.all()
    available_teams = [team for team in all_teams if team.get_status() == 'available']
    
    # For each awaiting incident, sort teams by station proximity and get resources
    for incident in awaiting_incidents:
        # Sort teams: nearest station first, then others
        nearest_station = incident.nearest_station_id
        sorted_teams = []
        if nearest_station:
            # Teams from the nearest station
            station_teams = [t for t in available_teams if t.station_id == nearest_station]
            # Other teams
            other_teams = [t for t in available_teams if t.station_id != nearest_station]
            sorted_teams = station_teams + other_teams
        else:
            sorted_teams = available_teams
        
        # Add display info to each team
        for team in sorted_teams:
            team.is_recommended = (team.station_id == nearest_station)
            team.station_display = team.get_station_display()
        
        incident.sorted_teams = sorted_teams
        
        # Get resources from the nearest station
        if nearest_station:
            incident.station_resources = Resource.query.filter_by(station_id=nearest_station).all()
        else:
            incident.station_resources = []
    
    # Get all resources for map popups
    all_resources = Resource.query.all()
    
    now = datetime.now()
    return render_template(
        'operations/live.html',
        title='Оперативен център',
        all_incidents=all_incidents,
        awaiting_incidents=awaiting_incidents,
        active_incidents=active_incidents,
        available_teams=available_teams,
        all_teams=all_teams,
        all_resources=all_resources,
        now=now
    )

@operations_bp.route('/tasks')
@login_required
@staff_required
def task_board():
    incidents = Incident.query.order_by(Incident.created_at.desc()).all()
    return render_template('operations/task_board.html', title='Табло за задачи', incidents=incidents)

@operations_bp.route('/map')
@login_required
@staff_required
def map_control():
    incidents = Incident.query.all()
    teams = Team.query.all()
    return render_template('operations/map_control.html', title='Карта', incidents=incidents, teams=teams)

@operations_bp.route('/api/incidents')
@login_required
@staff_required
def api_incidents():
    incidents = Incident.query.all()
    data = []
    for incident in incidents:
        data.append({
            'id': incident.id,
            'title': incident.title,
            'type': incident.type,
            'status': incident.status,
            'priority': incident.priority,
            'latitude': incident.latitude,
            'longitude': incident.longitude,
            'address': incident.address,
            'created_at': incident.created_at.isoformat(),
            'assigned_team_id': incident.assigned_team_id,
            'assigned_team_name': incident.assigned_team.name if incident.assigned_team else None,
            'attachment_filename': incident.attachment_filename,
            'attachment_path': incident.attachment_path,
            'nearest_station_id': incident.nearest_station_id,
            'nearest_station_name': incident.get_nearest_station_display()
        })
    return jsonify(data)

@operations_bp.route('/api/teams')
@login_required
@staff_required
def api_teams():
    teams = Team.query.all()
    data = []
    for team in teams:
        data.append({
            'id': team.id,
            'name': team.name,
            'station_id': team.station_id,
            'station_display': team.get_station_display(),
            'status': team.get_status_display(),
            'member_count': len(team.members)
        })
    return jsonify(data)

@operations_bp.route('/api/resources')
@login_required
@staff_required
def api_resources():
    resources = Resource.query.all()
    data = []
    for resource in resources:
        data.append({
            'id': resource.id,
            'name': resource.name,
            'quantity': resource.quantity,
            'station_id': resource.station_id,
            'station_display': resource.get_station_display()
        })
    return jsonify(data)