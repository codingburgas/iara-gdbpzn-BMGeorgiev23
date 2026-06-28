// Dashboard JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Initialize any dashboard widgets
    initializeStatsAnimation();
    initializeActivityFeed();
});

function initializeStatsAnimation() {
    // Animate stat numbers counting up
    const statNumbers = document.querySelectorAll('.stat-number');
    
    statNumbers.forEach(function(el) {
        const text = el.textContent;
        const number = parseInt(text.replace(/[^0-9]/g, ''));
        
        if (!isNaN(number) && number > 0) {
            let current = 0;
            const increment = Math.ceil(number / 30);
            const duration = 800;
            const stepTime = duration / 30;
            
            const timer = setInterval(function() {
                current += increment;
                if (current >= number) {
                    current = number;
                    clearInterval(timer);
                }
                el.textContent = current;
            }, stepTime);
        }
    });
}

function initializeActivityFeed() {
    // Auto-refresh activity feed (simulated)
    const activityContainer = document.querySelector('.card-body.p-0');
    if (activityContainer) {
        // In production, this would use WebSocket or API polling
        console.log('Activity feed initialized');
    }
}

// Team status tooltips
document.addEventListener('DOMContentLoaded', function() {
    const statusBadges = document.querySelectorAll('.status-badge');
    statusBadges.forEach(function(badge) {
        badge.addEventListener('mouseenter', function() {
            this.style.opacity = '0.8';
        });
        badge.addEventListener('mouseleave', function() {
            this.style.opacity = '1';
        });
    });
});