from flask import render_template, jsonify, request
from flask_login import login_required
from . import incidents_bp

@incidents_bp.route('/')
@login_required
def list_incidents():
    return render_template('incidents/list.html', title='Произшествия')

@incidents_bp.route('/create')
@login_required
def create_incident():
    return render_template('incidents/create.html', title='Ново произшествие')

@incidents_bp.route('/api/test')
def api_test():
    return jsonify({'status': 'OK', 'message': 'API работи!'})
