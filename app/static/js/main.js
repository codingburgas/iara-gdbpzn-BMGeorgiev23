// Theme Toggle
document.addEventListener('DOMContentLoaded', function() {
    // Check for saved theme preference
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        document.documentElement.setAttribute('data-theme', savedTheme);
    }
    
    // Create theme toggle button if it doesn't exist
    const navbar = document.querySelector('.navbar');
    if (navbar && !document.getElementById('themeToggle')) {
        const toggleBtn = document.createElement('button');
        toggleBtn.id = 'themeToggle';
        toggleBtn.className = 'theme-toggle';
        toggleBtn.setAttribute('aria-label', 'Toggle theme');
        toggleBtn.innerHTML = getThemeIcon();
        
        // Find the navbar-nav and append
        const nav = navbar.querySelector('.navbar-nav');
        if (nav) {
            const li = document.createElement('li');
            li.className = 'nav-item';
            li.appendChild(toggleBtn);
            nav.appendChild(li);
        }
        
        toggleBtn.addEventListener('click', function() {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            this.innerHTML = getThemeIcon();
        });
    }
    
    function getThemeIcon() {
        const theme = document.documentElement.getAttribute('data-theme');
        if (theme === 'dark') {
            return '<i class="fas fa-sun"></i>';
        }
        return '<i class="fas fa-moon"></i>';
    }
});

// Intersection Observer for scroll animations
document.addEventListener('DOMContentLoaded', function() {
    const animatedElements = document.querySelectorAll('.animate-fade-in, .animate-slide-up, .animate-pop-in');
    
    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                }
            });
        }, { threshold: 0.1 });
        
        animatedElements.forEach(function(el) {
            observer.observe(el);
        });
    }
});

// Navbar scroll effect
document.addEventListener('DOMContentLoaded', function() {
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                navbar.classList.add('navbar-scrolled');
            } else {
                navbar.classList.remove('navbar-scrolled');
            }
        });
    }
});