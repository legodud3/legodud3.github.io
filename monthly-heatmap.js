(function () {
    const MONTH_LABELS = ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'];
    const MONTH_NAMES = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

    function toMonthKey(dateValue) {
        if (typeof dateValue !== 'string') return null;
        const match = dateValue.match(/^(\d{4})-(\d{2})-\d{2}$/);
        if (!match) return null;
        const year = Number(match[1]);
        const monthIndex = Number(match[2]) - 1;
        if (!Number.isInteger(year) || monthIndex < 0 || monthIndex > 11) return null;
        return { year, monthIndex };
    }

    function getLevel(count, maxCount) {
        if (count <= 0 || maxCount <= 0) return 0;
        if (count === maxCount) return 4;
        const ratio = count / maxCount;
        if (ratio >= 0.75) return 3;
        if (ratio >= 0.4) return 2;
        return 1;
    }

    function createCell(year, monthIndex, count, level) {
        const cell = document.createElement('div');
        cell.className = `heatmap-cell heatmap-level-${level}`;
        const label = `${year}-${String(monthIndex + 1).padStart(2, '0')} (${MONTH_NAMES[monthIndex]} ${year}): ${count} post${count === 1 ? '' : 's'}`;
        cell.title = label;
        cell.setAttribute('role', 'img');
        cell.setAttribute('aria-label', label);
        return cell;
    }

    function renderHeatmap(root, posts) {
        const counts = new Map();
        let maxCount = 0;

        posts.forEach((post) => {
            const parsed = toMonthKey(post.date);
            if (!parsed) return;
            const key = `${parsed.year}-${parsed.monthIndex}`;
            const newCount = (counts.get(key) || 0) + 1;
            counts.set(key, newCount);
            if (newCount > maxCount) maxCount = newCount;
        });

        const yearSet = new Set();
        counts.forEach((_, key) => {
            const year = Number(key.split('-')[0]);
            if (Number.isInteger(year)) yearSet.add(year);
        });

        if (yearSet.size === 0) {
            root.innerHTML = '<p class="heatmap-empty">No post data yet.</p>';
            return;
        }

        const years = Array.from(yearSet).sort((a, b) => b - a);
        const widget = document.createElement('div');
        widget.className = 'heatmap-widget';

        const monthHeader = document.createElement('div');
        monthHeader.className = 'heatmap-months';

        const monthCorner = document.createElement('span');
        monthCorner.className = 'heatmap-corner';
        monthHeader.appendChild(monthCorner);

        MONTH_LABELS.forEach((month) => {
            const label = document.createElement('span');
            label.className = 'heatmap-month-label';
            label.textContent = month;
            monthHeader.appendChild(label);
        });
        widget.appendChild(monthHeader);

        years.forEach((year) => {
            const row = document.createElement('div');
            row.className = 'heatmap-row';

            const yearLabel = document.createElement('span');
            yearLabel.className = 'heatmap-year-label';
            yearLabel.textContent = year;
            row.appendChild(yearLabel);

            for (let monthIndex = 0; monthIndex < 12; monthIndex += 1) {
                const key = `${year}-${monthIndex}`;
                const count = counts.get(key) || 0;
                const level = getLevel(count, maxCount);
                row.appendChild(createCell(year, monthIndex, count, level));
            }

            widget.appendChild(row);
        });

        const legend = document.createElement('div');
        legend.className = 'heatmap-legend';
        legend.innerHTML = `
            <span>Less</span>
            <span class="heatmap-cell heatmap-level-0" aria-hidden="true"></span>
            <span class="heatmap-cell heatmap-level-1" aria-hidden="true"></span>
            <span class="heatmap-cell heatmap-level-2" aria-hidden="true"></span>
            <span class="heatmap-cell heatmap-level-3" aria-hidden="true"></span>
            <span class="heatmap-cell heatmap-level-4" aria-hidden="true"></span>
            <span>More</span>
        `;
        widget.appendChild(legend);

        root.innerHTML = '';
        root.appendChild(widget);
    }

    async function mountHeatmap(root) {
        root.innerHTML = '<p class="heatmap-empty">Loading writing heatmap...</p>';

        try {
            const response = await fetch('posts.json?v=' + Date.now());
            if (!response.ok) throw new Error('Failed to load posts.json');
            const posts = await response.json();
            renderHeatmap(root, Array.isArray(posts) ? posts : []);
        } catch (error) {
            console.error('Heatmap error:', error);
            root.innerHTML = '<p class="heatmap-empty">Could not load writing heatmap.</p>';
        }
    }

    function init() {
        const roots = document.querySelectorAll('.monthly-heatmap-root');
        if (!roots.length) return;
        roots.forEach((root) => {
            mountHeatmap(root);
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
