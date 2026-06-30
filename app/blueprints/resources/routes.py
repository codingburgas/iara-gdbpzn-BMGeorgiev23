from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from . import resources_bp
from app import db
from app.models.resource import Resource
from app.models.incident import Incident
from app.models.team import Team
from app.utils.decorators import staff_required, admin_required, role_required

@resources_bp.route('/')
@login_required
@staff_required
def inventory():
    resources = Resource.query.order_by(Resource.category, Resource.name).all()
    categories = db.session.query(Resource.category).distinct().all()
    return render_template('resources/inventory.html', title='Инвентар', resources=resources, categories=categories)

@resources_bp.route('/create', methods=['GET', 'POST'])
@login_required
@role_required(['admin', 'incident_manager'])
def create_resource():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        category = request.form.get('category')
        quantity = int(request.form.get('quantity', 0))
        unit = request.form.get('unit', 'бр.')
        status = request.form.get('status', 'available')
        location = request.form.get('location')
        
        if not name or not category:
            flash('Името и категорията са задължителни.', 'danger')
            return render_template('resources/create.html')
        
        resource = Resource(
            name=name,
            description=description,
            category=category,
            quantity=quantity,
            unit=unit,
            status=status,
            location=location
        )
        
        db.session.add(resource)
        db.session.commit()
        
        flash('Ресурсът е създаден успешно.', 'success')
        return redirect(url_for('resources.inventory'))
    
    return render_template('resources/create.html')

@resources_bp.route('/<int:resource_id>/edit', methods=['GET', 'POST'])
@login_required
@role_required(['admin', 'incident_manager'])
def edit_resource(resource_id):
    resource = Resource.query.get_or_404(resource_id)
    
    if request.method == 'POST':
        resource.name = request.form.get('name')
        resource.description = request.form.get('description')
        resource.category = request.form.get('category')
        resource.quantity = int(request.form.get('quantity', 0))
        resource.unit = request.form.get('unit', 'бр.')
        resource.status = request.form.get('status')
        resource.location = request.form.get('location')
        resource.last_updated = datetime.utcnow()
        
        db.session.commit()
        flash('Ресурсът е обновен успешно.', 'success')
        return redirect(url_for('resources.inventory'))
    
    return render_template('resources/edit.html', resource=resource)

@resources_bp.route('/<int:resource_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_resource(resource_id):
    resource = Resource.query.get_or_404(resource_id)
    db.session.delete(resource)
    db.session.commit()
    flash('Ресурсът е изтрит.', 'success')
    return redirect(url_for('resources.inventory'))

@resources_bp.route('/requests')
@login_required
@staff_required
def requests():
    incidents = Incident.query.filter(Incident.status.in_(['active', 'in_progress'])).all()
    resources = Resource.query.filter_by(status='available').all()
    return render_template('resources/requests.html', title='Заявки за ресурси', incidents=incidents, resources=resources)

@resources_bp.route('/logistics')
@login_required
@staff_required
def logistics():
    resources = Resource.query.all()
    return render_template('resources/logistics.html', title='Логистика', resources=resources)

@resources_bp.route('/api/data')
@login_required
@staff_required
def api_resources():
    resources = Resource.query.all()
    data = []
    for resource in resources:
        data.append({
            'id': resource.id,
            'name': resource.name,
            'category': resource.get_category_display(),
            'quantity': resource.quantity,
            'unit': resource.unit,
            'status': resource.get_status_display(),
            'location': resource.location or 'Не е указано',
            'last_updated': resource.last_updated.strftime('%d.%m.%Y %H:%M')
        })
    return jsonify(data)

@resources_bp.route('/<int:resource_id>/update-quantity', methods=['POST'])
@login_required
@staff_required
def update_quantity(resource_id):
    resource = Resource.query.get_or_404(resource_id)
    data = request.json
    quantity = data.get('quantity')
    
    if quantity is not None:
        resource.quantity = quantity
        resource.last_updated = datetime.utcnow()
        db.session.commit()
        return jsonify({'success': True, 'new_quantity': resource.quantity})
    
    return jsonify({'success': False, 'error': 'Invalid quantity'}), 400

@resources_bp.route('/<int:resource_id>/assign', methods=['POST'])
@login_required
@staff_required
def assign_resource(resource_id):
    resource = Resource.query.get_or_404(resource_id)
    data = request.json
    
    incident_id = data.get('incident_id')
    team_id = data.get('team_id')
    
    if incident_id:
        resource.assigned_incident_id = incident_id
        resource.status = 'in_use'
    elif team_id:
        resource.assigned_team_id = team_id
        resource.status = 'in_use'
    else:
        return jsonify({'success': False, 'error': 'No assignment specified'}), 400
    
    db.session.commit()
    return jsonify({'success': True})