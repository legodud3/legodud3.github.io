// Theme toggle functionality for CMYK modes
const themeSlider = document.getElementById('themeSlider');
const htmlElement = document.documentElement;

// Theme mapping: 0=dark, 1=cyan, 2=magenta, 3=yellow, 4=light
const themes = ['dark', 'cyan', 'magenta', 'yellow', 'light'];

// Ensure the theme slider element exists before proceeding
if (themeSlider) {
    // Check for saved theme preference or default to dark mode
    const currentTheme = localStorage.getItem('theme') || 'dark';
    const themeIndex = themes.indexOf(currentTheme);
    
    if (themeIndex !== -1) {
        themeSlider.value = themeIndex;
        applyTheme(currentTheme);
    } else {
        themeSlider.value = 0;
        applyTheme('dark');
    }

    // Handle slider change
    themeSlider.addEventListener('input', function() {
        const selectedTheme = themes[parseInt(this.value)];
        applyTheme(selectedTheme);
        localStorage.setItem('theme', selectedTheme);
    });
}

function applyTheme(theme) {
    // Remove all theme classes
    htmlElement.classList.remove('light-mode', 'cyan-mode', 'magenta-mode', 'yellow-mode');
    
    // Add the appropriate class for the theme (dark is default, no class needed)
    if (theme !== 'dark') {
        htmlElement.classList.add(`${theme}-mode`);
    }
}
