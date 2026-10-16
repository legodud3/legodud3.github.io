// Theme toggle. The inline <head> snippet has already applied either
// `light-mode` or `dark-mode` (honouring localStorage first, then the OS
// preference), so this only keeps that class in sync with the switch.
const themeToggle = document.getElementById('themeToggle');
const htmlElement = document.documentElement;

function prefersLight() {
    return !!(window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches);
}

function storedTheme() {
    try {
        return localStorage.getItem('theme');
    } catch (e) {
        return null;
    }
}

// Always leaves exactly one theme class on <html>, matching the head snippet's
// invariant so the CSS light palette stays the single source of truth.
function applyTheme(theme) {
    htmlElement.classList.toggle('light-mode', theme === 'light');
    htmlElement.classList.toggle('dark-mode', theme !== 'light');
}

if (themeToggle) {
    const saved = storedTheme();
    const isLight = saved === 'light' || (!saved && prefersLight());

    applyTheme(isLight ? 'light' : 'dark');
    themeToggle.checked = isLight;

    themeToggle.addEventListener('change', function () {
        const theme = this.checked ? 'light' : 'dark';
        applyTheme(theme);
        try {
            localStorage.setItem('theme', theme);
        } catch (e) {
            // Storage blocked (private mode / strict settings) — the theme still
            // applies for this page view, it just won't persist.
        }
    });
}
