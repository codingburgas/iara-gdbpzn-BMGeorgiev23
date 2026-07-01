// Theme Management
document.addEventListener('DOMContentLoaded', function() {
    initializeTheme();
    createThemeToggle();
});

function initializeTheme() {
    // Check for saved theme preference
    var savedTheme = localStorage.getItem('theme');
    var prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    // Set initial theme - already set by the script in head, but ensure consistency
    if (savedTheme) {
        document.documentElement.setAttribute('data-theme', savedTheme);
        updateThemeIcon(savedTheme);
    } else if (prefersDark) {
        document.documentElement.setAttribute('data-theme', 'dark');
        updateThemeIcon('dark');
    } else {
        document.documentElement.setAttribute('data-theme', 'light');
        updateThemeIcon('light');
    }
}

function createThemeToggle() {
    var navbar = document.querySelector('.navbar .navbar-nav');
    if (!navbar) return;
    
    if (document.getElementById('themeToggle')) return;
    
    var li = document.createElement('li');
    li.className = 'nav-item';
    
    var button = document.createElement('button');
    button.id = 'themeToggle';
    button.className = 'nav-link theme-toggle';
    button.setAttribute('aria-label', 'Toggle theme');
    button.style.background = 'none';
    button.style.border = 'none';
    button.style.cursor = 'pointer';
    
    var currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
    button.innerHTML = currentTheme === 'dark' 
        ? '<i class="fas fa-sun"></i>' 
        : '<i class="fas fa-moon"></i>';
    
    button.addEventListener('click', function() {
        toggleTheme();
    });
    
    li.appendChild(button);
    navbar.appendChild(li);
}

function toggleTheme() {
    var currentTheme = document.documentElement.getAttribute('data-theme');
    var newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeIcon(newTheme);
}

function updateThemeIcon(theme) {
    var toggle = document.getElementById('themeToggle');
    if (toggle) {
        toggle.innerHTML = theme === 'dark' 
            ? '<i class="fas fa-sun"></i>' 
            : '<i class="fas fa-moon"></i>';
    }
}

// Listen for system theme changes
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function(e) {
    if (!localStorage.getItem('theme')) {
        var newTheme = e.matches ? 'dark' : 'light';
        document.documentElement.setAttribute('data-theme', newTheme);
        updateThemeIcon(newTheme);
    }
});

// Export for use in other files
window.toggleTheme = toggleTheme;