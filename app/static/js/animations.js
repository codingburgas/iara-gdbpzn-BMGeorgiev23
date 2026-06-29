// Animation Controller
document.addEventListener('DOMContentLoaded', function() {
    initializeScrollAnimations();
    initializeCounterAnimations();
    initializeHoverAnimations();
});

// ============ SCROLL ANIMATIONS ============

function initializeScrollAnimations() {
    const elements = document.querySelectorAll('.scroll-fade-in, .animate-on-scroll');
    
    if (elements.length === 0) return;
    
    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });
        
        elements.forEach(function(el) {
            observer.observe(el);
        });
    } else {
        // Fallback for older browsers
        elements.forEach(function(el) {
            el.classList.add('visible');
            el.style.opacity = '1';
            el.style.transform = 'translateY(0)';
        });
    }
}

// ============ COUNTER ANIMATIONS ============

function initializeCounterAnimations() {
    const counters = document.querySelectorAll('.counter');
    
    counters.forEach(function(counter) {
        const target = parseInt(counter.getAttribute('data-target')) || 0;
        const duration = parseInt(counter.getAttribute('data-duration')) || 1500;
        const stepTime = 30;
        const steps = duration / stepTime;
        const increment = target / steps;
        let current = 0;
        
        const observer = new IntersectionObserver(function(entries) {
            if (entries[0].isIntersecting) {
                startCounter();
                observer.unobserve(counter);
            }
        }, { threshold: 0.5 });
        
        observer.observe(counter);
        
        function startCounter() {
            const timer = setInterval(function() {
                current += increment;
                if (current >= target) {
                    current = target;
                    clearInterval(timer);
                }
                counter.textContent = Math.round(current);
            }, stepTime);
        }
    });
}

// ============ HOVER ANIMATIONS ============

function initializeHoverAnimations() {
    // Add hover classes to elements with data-hover attribute
    document.querySelectorAll('[data-hover]').forEach(function(el) {
        const animation = el.dataset.hover;
        el.addEventListener('mouseenter', function() {
            this.classList.add('hover-' + animation);
        });
        el.addEventListener('mouseleave', function() {
            this.classList.remove('hover-' + animation);
        });
    });
}

// ============ SEQUENTIAL ANIMATIONS ============

function animateSequential(selector, className, delay) {
    const elements = document.querySelectorAll(selector);
    delay = delay || 100;
    
    elements.forEach(function(el, index) {
        setTimeout(function() {
            el.classList.add(className);
        }, index * delay);
    });
}

// ============ UTILITY FUNCTIONS ============

function triggerAnimation(element, animationClass) {
    element.classList.remove(animationClass);
    // Force reflow
    void element.offsetWidth;
    element.classList.add(animationClass);
}

function animateOnClick(selector, animationClass) {
    document.querySelectorAll(selector).forEach(function(el) {
        el.addEventListener('click', function() {
            triggerAnimation(this, animationClass);
        });
    });
}

// Export for use in other files
window.animateSequential = animateSequential;
window.triggerAnimation = triggerAnimation;
window.animateOnClick = animateOnClick;