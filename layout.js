// Shared layout module: builds the left rail (brand, nav, heatmap widget) and
// the site footer so each page only carries its unique content.
//
// Mount points:
//   <aside class="left-rail" data-layout-rail></aside>
//   <footer class="site-footer" data-layout-footer></footer>
//   (use data-layout-footer="minimal" to omit the writing-desk link)
//
// The active nav item comes from <body data-page="home|about|projects">.
// Paths are root-absolute so generated pages under /p/ resolve correctly.
// Load this BEFORE monthly-heatmap.js and theme-toggle.js so the heatmap mount
// point and #themeToggle exist when those scripts initialize.
window.Layout = (function () {
    const NAV_ITEMS = [
        { key: 'home', href: '/index.html', icon: 'ð ', label: 'Home' },
        { key: 'about', href: '/about.html', icon: 'ð¤', label: 'About me' },
        { key: 'projects', href: '/side-projects.html', icon: 'ð', label: 'Side projects' },
    ];

    function el(tag, className, text) {
        const node = document.createElement(tag);
        if (className) node.className = className;
        if (text !== undefined) node.textContent = text;
        return node;
    }

    function buildRail(rail, activePage) {
        const brand = el('a', 'rail-brand');
        brand.href = '/index.html';
        const logo = el('img', 'site-logo');
        logo.src = '/legohat_logo.png';
        logo.alt = 'Logo';
        brand.appendChild(logo);
        brand.appendChild(el('span', null, 'Chinmay Deo'));
        rail.appendChild(brand);

        const nav = el('nav', 'rail-nav');
        nav.setAttribute('aria-label', 'Primary');
        NAV_ITEMS.forEach((item) => {
            const link = el('a', item.key === activePage ? 'active' : null);
            link.href = item.href;
            const icon = el('span', null, item.icon);
            icon.setAttribute('aria-hidden', 'true');
            link.appendChild(icon);
            link.appendChild(document.createTextNode(' ' + item.label));
            nav.appendChild(link);
        });
        rail.appendChild(nav);

        const widget = el('section', 'rail-widget');
        widget.appendChild(el('h2', 'rail-section-title', 'Writing Consistency'));
        const heatmapRoot = el('div', 'monthly-heatmap-root');
        heatmapRoot.setAttribute('aria-live', 'polite');
        widget.appendChild(heatmapRoot);
        const hatTip = el('p', 'rail-hat-tip', 'Hat tip to ');
        const githubLink = el('a', null, 'GitHub');
        githubLink.href = 'https://github.com';
        githubLink.target = '_blank';
        githubLink.rel = 'noopener noreferrer';
        hatTip.appendChild(githubLink);
        hatTip.appendChild(document.createTextNode(' for the original contribution graph inspiration.'));
        widget.appendChild(hatTip);
        rail.appendChild(widget);
    }

    function buildFooter(footer, variant) {
        footer.appendChild(el('p', null,
            'All writing is personal. Views are my own and do not represent my employer, friends, or family.'));

        if (variant !== 'minimal') {
            const desk = el('a', 'writing-desk-link', 'Open the writing desk');
            desk.href = '/write.html';
            footer.appendChild(desk);
        }

        const toggle = el('div', 'theme-toggle-container');
        toggle.appendChild(el('span', 'theme-toggle-label', 'Dark'));
        const switchLabel = el('label', 'theme-toggle-switch');
        const input = document.createElement('input');
        input.type = 'checkbox';
        input.id = 'themeToggle';
        input.setAttribute('role', 'switch');
        input.setAttribute('aria-label', 'Toggle between dark and light theme');
        switchLabel.appendChild(input);
        switchLabel.appendChild(el('span', 'theme-toggle-slider'));
        toggle.appendChild(switchLabel);
        toggle.appendChild(el('span', 'theme-toggle-label', 'Light'));
        footer.appendChild(toggle);
    }

    function mount() {
        const activePage = document.body ? document.body.getAttribute('data-page') : null;
        document.querySelectorAll('[data-layout-rail]').forEach((rail) => {
            rail.innerHTML = '';
            buildRail(rail, activePage);
        });
        document.querySelectorAll('[data-layout-footer]').forEach((footer) => {
            footer.innerHTML = '';
            buildFooter(footer, footer.getAttribute('data-layout-footer'));
        });
    }

    // Loaded at the end of <body>, so mount points are usually already parsed.
    if (document.querySelector('[data-layout-rail], [data-layout-footer]')) {
        mount();
    } else {
        document.addEventListener('DOMContentLoaded', mount);
    }

    return { mount };
})();

// Google Analytics (GA4)
(function () {
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=G-0R7GSH6T00';
    document.head.appendChild(s);
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    window.gtag = gtag;
    gtag('js', new Date());
    gtag('config', 'G-0R7GSH6T00');
})();
