// Theme Management
document.addEventListener('DOMContentLoaded', function() {
    initializeTheme();
    createThemeToggle();
});

function initializeTheme() {
    // Check for saved theme preference
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    // Set initial theme
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
    const navbar = document.querySelector('.navbar .navbar-nav');
    if (!navbar) return;
    
    // Check if toggle already exists
    if (document.getElementById('themeToggle')) return;
    
    const li = document.createElement('li');
    li.className = 'nav-item';
    
    const button = document.createElement('button');
    button.id = 'themeToggle';
    button.className = 'nav-link theme-toggle';
    button.setAttribute('aria-label', 'Toggle theme');
    button.style.background = 'none';
    button.style.border = 'none';
    button.style.cursor = 'pointer';
    
    const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
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
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeIcon(newTheme);
}

function updateThemeIcon(theme) {
    const toggle = document.getElementById('themeToggle');
    if (toggle) {
        toggle.innerHTML = theme === 'dark' 
            ? '<i class="fas fa-sun"></i>' 
            : '<i class="fas fa-moon"></i>';
    }
}

// Listen for system theme changes
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function(e) {
    if (!localStorage.getItem('theme')) {
        const newTheme = e.matches ? 'dark' : 'light';
        document.documentElement.setAttribute('data-theme', newTheme);
        updateThemeIcon(newTheme);
    }
});

// Export for use in other files
window.toggleTheme = toggleTheme;