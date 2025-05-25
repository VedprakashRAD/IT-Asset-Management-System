/**
 * IT Asset Management System - Theme Management
 * Modern theme toggle functionality with system preference detection
 */

document.addEventListener('DOMContentLoaded', function() {
    // Theme constants
    const THEME_STORAGE_KEY = 'itam-theme';
    const DARK_THEME = 'dark';
    const LIGHT_THEME = 'light';
    
    // DOM elements
    const themeToggle = document.getElementById('theme-toggle');
    const themeIcon = themeToggle ? themeToggle.querySelector('i') : null;
    
    // Theme detection and initialization
    function initTheme() {
        if (!themeToggle || !themeIcon) return;
        
        const savedTheme = localStorage.getItem(THEME_STORAGE_KEY);
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        
        // Set initial theme based on saved preference or system preference
        if (savedTheme === DARK_THEME || (!savedTheme && prefersDark)) {
            applyTheme(DARK_THEME);
        } else {
            applyTheme(LIGHT_THEME);
        }
        
        // Listen for system preference changes
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
            // Only change if user hasn't set a preference
            if (!localStorage.getItem(THEME_STORAGE_KEY)) {
                applyTheme(e.matches ? DARK_THEME : LIGHT_THEME);
            }
        });
        
        // Toggle theme on click
        themeToggle.addEventListener('click', toggleTheme);
    }
    
    // Apply theme to document
    function applyTheme(theme) {
        if (theme === DARK_THEME) {
            document.body.classList.add('dark-theme');
            if (themeIcon) updateIcon(DARK_THEME);
        } else {
            document.body.classList.remove('dark-theme');
            if (themeIcon) updateIcon(LIGHT_THEME);
        }
    }
    
    // Toggle between light and dark themes
    function toggleTheme() {
        const isDark = document.body.classList.contains('dark-theme');
        const newTheme = isDark ? LIGHT_THEME : DARK_THEME;
        
        // Apply the theme
        applyTheme(newTheme);
        
        // Save user preference
        localStorage.setItem(THEME_STORAGE_KEY, newTheme);
        
        // Animate icon
        animateIcon();
    }
    
    // Update icon based on current theme
    function updateIcon(theme) {
        if (!themeIcon) return;
        
        if (theme === DARK_THEME) {
            themeIcon.classList.replace('bi-sun-fill', 'bi-moon-fill');
        } else {
            themeIcon.classList.replace('bi-moon-fill', 'bi-sun-fill');
        }
    }
    
    // Animate icon on toggle
    function animateIcon() {
        if (!themeIcon) return;
        
        themeIcon.style.animation = 'none';
        setTimeout(() => {
            themeIcon.style.animation = '';
        }, 10);
    }
    
    // Initialize theme
    initTheme();
}); 