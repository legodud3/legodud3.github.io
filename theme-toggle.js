// Theme toggle functionality
const themeToggle = document.getElementById('themeToggle');
const htmlElement = document.documentElement;

// Check for saved theme preference or default to dark mode
const currentTheme = localStorage.getItem('theme');
if (currentTheme === 'light') {
    htmlElement.classList.add('light-mode');
    themeToggle.checked = true;
}

// Toggle theme when switch is clicked
themeToggle.addEventListener('change', function() {
    if (this.checked) {
        htmlElement.classList.add('light-mode');
        localStorage.setItem('theme', 'light');
    } else {
        htmlElement.classList.remove('light-mode');
        localStorage.setItem('theme', 'dark');
    }
});
