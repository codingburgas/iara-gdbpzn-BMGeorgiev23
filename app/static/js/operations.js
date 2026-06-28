// Operations JavaScript
document.addEventListener('DOMContentLoaded', function() {
    initializeOperationsMap();
    initializeTaskDragDrop();
    initializeStatusUpdates();
});

function initializeOperationsMap() {
    const mapContainer = document.getElementById('operations-map') || document.getElementById('full-map');
    if (mapContainer && typeof L !== 'undefined') {
        const map = L.map(mapContainer).setView([42.6977, 23.3219], 12);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors'
        }).addTo(map);
        
        // Add incident markers (example)
        fetch('/operations/api/incidents')
            .then(response => response.json())
            .then(data => {
                data.forEach(function(incident) {
                    if (incident.latitude && incident.longitude) {
                        var color = incident.status === 'active' ? 'red' :
                                   incident.status === 'in_progress' ? 'orange' : 'green';
                        L.circleMarker([incident.latitude, incident.longitude], {
                            radius: 10,
                            color: color,
                            fillColor: color,
                            fillOpacity: 0.7
                        }).addTo(map)
                        .bindPopup(
                            '<b>' + incident.title + '</b><br>' +
                            incident.address + '<br>' +
                            'Статус: ' + incident.status
                        );
                    }
                });
            })
            .catch(error => console.log('Map data error:', error));
    }
}

function initializeTaskDragDrop() {
    // Placeholder for drag-and-drop functionality
    console.log('Task board drag-and-drop initialized');
}

function initializeStatusUpdates() {
    // Auto-refresh status every 30 seconds
    setInterval(function() {
        // In production, this would update status via API
        console.log('Checking for updates...');
    }, 30000);
}

// Export functions for use in templates
window.centerMap = function() {
    console.log('Centering map...');
};

window.refreshMap = function() {
    console.log('Refreshing map...');
    initializeOperationsMap();
};