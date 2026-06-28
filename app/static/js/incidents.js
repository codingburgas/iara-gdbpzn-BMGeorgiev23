// Incidents JavaScript
document.addEventListener('DOMContentLoaded', function() {
    initializeStatusUpdates();
    initializeMap();
});

function initializeStatusUpdates() {
    const statusButtons = document.querySelectorAll('.update-status');
    statusButtons.forEach(function(btn) {
        btn.addEventListener('click', function() {
            const incidentId = this.dataset.id;
            const status = this.dataset.status;
            
            fetch('/incidents/' + incidentId + '/update-status', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({ status: status })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    location.reload();
                }
            });
        });
    });
}

function initializeMap() {
    const mapContainer = document.getElementById('incident-map');
    if (mapContainer && typeof L !== 'undefined') {
        const map = L.map('incident-map').setView([42.6977, 23.3219], 13);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap'
        }).addTo(map);
    }
}