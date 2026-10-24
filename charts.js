// charts.js — initializes Chart.js instances from <canvas data-chart> elements
// found in post pages. Chart.js is loaded via CDN (chart.umd.min.js) and exposes
// the global `Chart` constructor.
//
// Posts embed charts as fenced code blocks in Markdown:
//
//     ```chart
//     {
//       "type": "line",
//       "data": {
//         "labels": ["Jan", "Feb", "Mar"],
//         "datasets": [{ "label": "Users", "data": [10, 20, 15] }]
//       },
//       "options": { "responsive": true, "plugins": { "title": { "display": true, "text": "Users" } } }
//     }
//     ```
//
// update_posts.py converts those into <div class="chart-wrapper"><canvas data-chart="{json}"></canvas></div>
// and this script initializes them.
//
// Theme handling: explicit author-specified colours are preserved. Theme-aware
// defaults (axis text, grid, legend labels) are applied only when the author
// has not already set them. Each chart is initialized in its own error handler
// so one broken config never prevents sibling charts from rendering.
window.Charts = (function () {
    var instances = [];

    function isDark() {
        return document.documentElement.classList.contains('dark-mode');
    }

    function prefersReducedMotion() {
        return (
            window.matchMedia &&
            window.matchMedia('(prefers-reduced-motion: reduce)').matches
        );
    }

    function themePalette(dark) {
        return {
            text: dark ? '#e8e6de' : '#1a1a1a',
            border: dark ? '#3a3a3a' : '#e0e0e0',
        };
    }

    // Set a value only if the author has not already provided one.
    function setIfAbsent(target, key, value) {
        if (target[key] === undefined) {
            target[key] = value;
        }
    }

    function applyThemeOverrides(config, dark) {
        var pal = themePalette(dark);
        var opts = config.options || (config.options = {});
        var plugins = opts.plugins || (opts.plugins = {});
        var legendVal = plugins.legend;
        var legendIsObject = legendVal && typeof legendVal === 'object';
        // Preserve explicit legend: false; otherwise ensure an object we can
        // safely add theme defaults to.
        var legend = legendIsObject ? legendVal : (legendVal !== false ? (plugins.legend = {}) : false);
        var title = plugins.title || (plugins.title = {});

        // Animation: honour prefers-reduced-motion at the Chart.js level so
        // JS-drawn animation stops, not just CSS opacity.
        if (prefersReducedMotion()) {
            opts.animation = false;
        }

        // Scales: apply theme colours only where the author hasn't set them.
        if (opts.scales) {
            Object.keys(opts.scales).forEach(function (key) {
                var scale = opts.scales[key];
                if (!scale) return;
                if (scale.ticks) setIfAbsent(scale.ticks, 'color', pal.text);
                if (scale.title) setIfAbsent(scale.title, 'color', pal.text);
                if (scale.grid) setIfAbsent(scale.grid, 'color', pal.border);
            });
        }

        // Legend: preserve explicit legend: false and explicit colours.
        if (legend && typeof legend === 'object' && legend.display !== false) {
            setIfAbsent(legend, 'labels', {});
            setIfAbsent(legend.labels, 'color', pal.text);
        }
        // Title: preserve explicit colours.
        if (title.display !== false) {
            setIfAbsent(title, 'color', pal.text);
        }
    }

    function create(canvas) {
        var json = canvas.getAttribute('data-chart');
        if (!json) return null;

        var config;
        try {
            config = JSON.parse(json);
        } catch (e) {
            console.error('Charts: invalid JSON in data-chart:', e);
            return null;
        }

        // Sensible defaults.
        config.options = config.options || {};
        if (config.options.responsive === undefined) config.options.responsive = true;
        if (config.options.maintainAspectRatio === undefined) config.options.maintainAspectRatio = false;

        applyThemeOverrides(config, isDark());

        var ctx = canvas.getContext('2d');
        var instance;
        try {
            instance = new Chart(ctx, config);
        } catch (e) {
            console.error('Charts: failed to render chart:', e);
            return null;
        }

        instances.push({ canvas: canvas, instance: instance, config: config });
        return instance;
    }

    function init() {
        if (typeof Chart === 'undefined') {
            console.warn('Charts: Chart.js not loaded yet.');
            return;
        }
        // Destroy any existing instances (e.g. re-init after theme change).
        instances.forEach(function (entry) {
            try { entry.instance.destroy(); } catch (e) {}
        });
        instances = [];

        document.querySelectorAll('canvas[data-chart]').forEach(create);
    }

    function refresh() {
        init();
    }

    // Expose.
    return {
        init: init,
        refresh: refresh,
    };
})();

// Auto-initialise once the DOM is ready.
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', window.Charts.init);
} else {
    window.Charts.init();
}

// Re-initialise charts when the theme toggles so colours stay on-palette.
var _themeMedia = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)');
if (_themeMedia) {
    _themeMedia.addEventListener('change', window.Charts.refresh);
}
// Also hook manual toggles via localStorage polling (simple, dependency-free).
(function () {
    var last = null;
    setInterval(function () {
        try {
            var cur = localStorage.getItem('theme');
            if (cur !== last) {
                last = cur;
                // Small delay so the theme class has time to flip.
                setTimeout(window.Charts.refresh, 50);
            }
        } catch (e) {}
    }, 1000);
})();
