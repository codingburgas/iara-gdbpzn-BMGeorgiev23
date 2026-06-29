// Reports JavaScript
let typeChart, statusChart, dailyChart, priorityChart, monthlyChart, teamChart, rateChart;

// ============ OVERVIEW ============

function loadOverviewData() {
    fetch('/reports/api/overview')
        .then(function(response) { return response.json(); })
        .then(function(data) {
            // Update stats
            document.getElementById('total-incidents').textContent = data.total_incidents;
            document.getElementById('active-incidents').textContent = data.active_incidents;
            document.getElementById('resolved-incidents').textContent = data.resolved_incidents;
            
            var rate = data.total_incidents > 0 
                ? Math.round((data.resolved_incidents / data.total_incidents) * 100) 
                : 0;
            document.getElementById('resolution-rate').textContent = rate + '%';
            
            // Update recent activity
            var tbody = document.getElementById('recent-activity');
            if (data.recent.length === 0) {
                tbody.innerHTML = '<tr><td colspan="4" class="text-center py-3 text-muted">Няма скорошна активност</td></tr>';
            } else {
                var html = '';
                data.recent.forEach(function(item) {
                    var statusBadge = item.status === 'active' ? 'danger' :
                                     item.status === 'in_progress' ? 'warning' :
                                     item.status === 'resolved' ? 'success' : 'secondary';
                    html += '<tr>' +
                        '<td>#' + item.id + '</td>' +
                        '<td>' + item.title + '</td>' +
                        '<td><span class="badge bg-' + statusBadge + '">' + item.status + '</span></td>' +
                        '<td>' + item.created_at + '</td>' +
                        '</tr>';
                });
                tbody.innerHTML = html;
            }
            
            // Create charts
            createOverviewCharts(data);
        })
        .catch(function(error) {
            console.log('Error loading overview data:', error);
        });
}

function createOverviewCharts(data) {
    // Type chart
    var typeCtx = document.getElementById('typeChart');
    if (typeCtx) {
        var typeLabels = [];
        var typeCounts = [];
        var typeColors = ['#dc3545', '#fd7e14', '#6c757d'];
        
        data.type_stats.forEach(function(item, index) {
            var label = item.type === 'fire' ? 'Пожар' :
                       item.type === 'rescue' ? 'Спасителна' : 'Друго';
            typeLabels.push(label);
            typeCounts.push(item.count);
        });
        
        if (typeChart) typeChart.destroy();
        typeChart = new Chart(typeCtx, {
            type: 'doughnut',
            data: {
                labels: typeLabels.length > 0 ? typeLabels : ['Няма данни'],
                datasets: [{
                    data: typeCounts.length > 0 ? typeCounts : [1],
                    backgroundColor: typeColors.slice(0, typeLabels.length || 1),
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { position: 'bottom' }
                }
            }
        });
    }
    
    // Status chart
    var statusCtx = document.getElementById('statusChart');
    if (statusCtx) {
        var statusLabels = [];
        var statusCounts = [];
        var statusColors = ['#dc3545', '#ffc107', '#28a745', '#6c757d'];
        
        data.status_stats.forEach(function(item) {
            var label = item.status === 'active' ? 'Активен' :
                       item.status === 'in_progress' ? 'В процес' :
                       item.status === 'resolved' ? 'Разрешен' : 'Затворен';
            statusLabels.push(label);
            statusCounts.push(item.count);
        });
        
        if (statusChart) statusChart.destroy();
        statusChart = new Chart(statusCtx, {
            type: 'pie',
            data: {
                labels: statusLabels.length > 0 ? statusLabels : ['Няма данни'],
                datasets: [{
                    data: statusCounts.length > 0 ? statusCounts : [1],
                    backgroundColor: statusColors.slice(0, statusLabels.length || 1),
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { position: 'bottom' }
                }
            }
        });
    }
}

// ============ INCIDENT ANALYTICS ============

function loadIncidentAnalytics() {
    var days = document.getElementById('days-filter').value;
    
    fetch('/reports/api/incidents-analytics?days=' + days)
        .then(function(response) { return response.json(); })
        .then(function(data) {
            document.getElementById('avg-resolution').textContent = data.avg_resolution_time || 0;
            createIncidentCharts(data);
        })
        .catch(function(error) {
            console.log('Error loading incident analytics:', error);
        });
}

function createIncidentCharts(data) {
    // Daily chart
    var dailyCtx = document.getElementById('dailyChart');
    if (dailyCtx) {
        var dates = data.daily_stats.map(function(item) { return item.date; });
        var counts = data.daily_stats.map(function(item) { return item.count; });
        
        if (dailyChart) dailyChart.destroy();
        dailyChart = new Chart(dailyCtx, {
            type: 'line',
            data: {
                labels: dates.length > 0 ? dates : ['Няма данни'],
                datasets: [{
                    label: 'Произшествия',
                    data: counts.length > 0 ? counts : [0],
                    borderColor: '#dc3545',
                    backgroundColor: 'rgba(220, 53, 69, 0.1)',
                    fill: true,
                    tension: 0.3
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: { stepSize: 1 }
                    }
                }
            }
        });
    }
    
    // Priority chart
    var priorityCtx = document.getElementById('priorityChart');
    if (priorityCtx) {
        var priorityLabels = [];
        var priorityCounts = [];
        var priorityColors = ['#dc3545', '#fd7e14', '#ffc107', '#28a745'];
        
        data.priority_stats.forEach(function(item) {
            var label = item.priority === 'critical' ? 'Критичен' :
                       item.priority === 'high' ? 'Висок' :
                       item.priority === 'medium' ? 'Среден' : 'Нисък';
            priorityLabels.push(label);
            priorityCounts.push(item.count);
        });
        
        if (priorityChart) priorityChart.destroy();
        priorityChart = new Chart(priorityCtx, {
            type: 'bar',
            data: {
                labels: priorityLabels.length > 0 ? priorityLabels : ['Няма данни'],
                datasets: [{
                    data: priorityCounts.length > 0 ? priorityCounts : [0],
                    backgroundColor: priorityColors.slice(0, priorityLabels.length || 1)
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: { stepSize: 1 }
                    }
                }
            }
        });
    }
    
    // Monthly chart
    var monthlyCtx = document.getElementById('monthlyChart');
    if (monthlyCtx) {
        var monthLabels = data.month_stats.map(function(item) {
            return item.month + '/' + item.year;
        });
        var monthCounts = data.month_stats.map(function(item) { return item.count; });
        
        if (monthlyChart) monthlyChart.destroy();
        monthlyChart = new Chart(monthlyCtx, {
            type: 'bar',
            data: {
                labels: monthLabels.length > 0 ? monthLabels : ['Няма данни'],
                datasets: [{
                    label: 'Произшествия',
                    data: monthCounts.length > 0 ? monthCounts : [0],
                    backgroundColor: 'rgba(13, 110, 253, 0.6)',
                    borderColor: '#0d6efd',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: { stepSize: 1 }
                    }
                }
            }
        });
    }
}

// ============ TEAM PERFORMANCE ============

function loadTeamPerformance() {
    fetch('/reports/api/team-performance')
        .then(function(response) { return response.json(); })
        .then(function(data) {
            createTeamCharts(data);
            updateTeamTable(data);
        })
        .catch(function(error) {
            console.log('Error loading team performance:', error);
        });
}

function createTeamCharts(data) {
    // Team chart
    var teamCtx = document.getElementById('teamChart');
    if (teamCtx) {
        var teamNames = data.teams.map(function(item) { return item.name || 'Без екип'; });
        var incidentCounts = data.teams.map(function(item) { return item.incident_count; });
        
        if (teamChart) teamChart.destroy();
        teamChart = new Chart(teamCtx, {
            type: 'bar',
            data: {
                labels: teamNames.length > 0 ? teamNames : ['Няма данни'],
                datasets: [{
                    label: 'Произшествия',
                    data: incidentCounts.length > 0 ? incidentCounts : [0],
                    backgroundColor: 'rgba(220, 53, 69, 0.6)',
                    borderColor: '#dc3545',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: { stepSize: 1 }
                    }
                }
            }
        });
    }
    
    // Rate chart
    var rateCtx = document.getElementById('rateChart');
    if (rateCtx) {
        var rateNames = data.teams.map(function(item) { return item.name || 'Без екип'; });
        var rates = data.teams.map(function(item) { return item.resolution_rate; });
        
        if (rateChart) rateChart.destroy();
        rateChart = new Chart(rateCtx, {
            type: 'bar',
            data: {
                labels: rateNames.length > 0 ? rateNames : ['Няма данни'],
                datasets: [{
                    label: 'Ефективност (%)',
                    data: rates.length > 0 ? rates : [0],
                    backgroundColor: function(context) {
                        var value = context.parsed.y;
                        return value >= 80 ? 'rgba(40, 167, 69, 0.6)' :
                               value >= 50 ? 'rgba(255, 193, 7, 0.6)' :
                               'rgba(220, 53, 69, 0.6)';
                    },
                    borderColor: function(context) {
                        var value = context.parsed.y;
                        return value >= 80 ? '#28a745' :
                               value >= 50 ? '#ffc107' :
                               '#dc3545';
                    },
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        ticks: { stepSize: 10, callback: function(value) { return value + '%'; } }
                    }
                }
            }
        });
    }
}

function updateTeamTable(data) {
    var tbody = document.getElementById('team-table-body');
    if (!tbody) return;
    
    if (data.teams.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="text-center py-3 text-muted">Няма създадени екипи</td></tr>';
        return;
    }
    
    var html = '';
    data.teams.forEach(function(team) {
        var statusBadge = team.status === 'active' ? 'success' :
                         team.status === 'on_mission' ? 'warning text-dark' : 'secondary';
        var statusText = team.status === 'active' ? 'Активен' :
                        team.status === 'on_mission' ? 'На мисия' : 'Неактивен';
        
        var rateColor = team.resolution_rate >= 80 ? 'success' :
                       team.resolution_rate >= 50 ? 'warning text-dark' : 'danger';
        
        html += '<tr>' +
            '<td><strong>' + team.name + '</strong></td>' +
            '<td>' + team.member_count + '</td>' +
            '<td><span class="badge bg-' + statusBadge + '">' + statusText + '</span></td>' +
            '<td>' + team.incident_count + '</td>' +
            '<td>' + team.active_incidents + '</td>' +
            '<td>' + team.resolved_incidents + '</td>' +
            '<td><span class="badge bg-' + rateColor + '">' + team.resolution_rate + '%</span></td>' +
            '</tr>';
    });
    tbody.innerHTML = html;
}

// ============ UTILITY FUNCTIONS ============

function refreshData() {
    loadOverviewData();
    loadIncidentAnalytics();
    loadTeamPerformance();
}