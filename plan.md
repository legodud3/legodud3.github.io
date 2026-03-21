# Blog UI Redesign — Implementation Plan

## 1. Typography Upgrade
**Files:** `style.css`
- Add Google Fonts import for a handwriting font (Caveat or Patrick Hand) as fallback instead of Comic Sans
- Add a serif font (Lora or Source Serif Pro) for body/reading text
- Update `--font-handwriting` fallback chain
- Update `body` font-family to use the serif for reading
- Bump `line-height` from 1.6 to 1.75

## 2. Color Palette — LEGO Gold Identity
**Files:** `style.css`
- Promote `#FFD700` (LEGO gold) to a CSS custom property `--accent-color`
- Apply gold accent to: `.rail-brand span`, `.surprise-btn` border/hover, active nav states
- Replace blue (`--link-color`) usage for brand/accent elements with gold (keep blue for hyperlinks)
- Add more tag color classes (prepare `tag-tech`, `tag-life`, etc. with distinct colors)
- Update `tags.json` with new tag entries and colors

## 3. Post List Visual Upgrade
**Files:** `index.html`, `style.css`
- Show 2-line excerpt below each post title (data already in `posts.json`)
- Restyle numbering: larger, lighter-weight numbers positioned as a visual feature (e.g., `2rem`, `color: #444`)
- Replace `border-bottom` dividers with subtle card containers (light bg on hover, `border-radius: 8px`, padding)
- Make the first/newest post visually larger (featured post treatment with bigger title + more excerpt)

## 4. Side Projects — Table to Cards
**Files:** `side-projects.html`, `style.css`
- Replace `<table>` with a card grid layout (reuse/extend `.related-post-card` pattern)
- Each card: title, description, action links (Live demo / Repo)
- Add colored left-border or accent per card for visual variety
- Add emoji/icon per project as a visual anchor

## 5. Search Input Styling
**Files:** `style.css`, `index.html`
- Add inline SVG magnifying glass icon inside search input (via `background-image` or a `::before` on a wrapper)
- Increase `border-radius` to 10px, padding to 12px 14px 12px 38px (room for icon)
- Add focus state: gold border/glow (`box-shadow`) using `--accent-color`

## 6. Transitions & Micro-interactions
**Files:** `style.css`, `view.html`, `monthly-heatmap.js`, `index.html`
- **Post content fade-in:** Add `.fade-in` class with `opacity 0→1` over 200ms, apply on view.html content load
- **Heatmap staggered fade:** Add CSS `@keyframes` for cell fade-in, apply with staggered `animation-delay` in JS
- **LEGO brick build animation:** On audio player creation, animate bricks appearing left-to-right (brief, ~400ms total)
- **Post list items:** Subtle staggered fade-in on render

## 7. Mobile Experience
**Files:** `style.css`, all HTML files (minor)
- At `@media (max-width: 940px)`: collapse left-rail into a compact horizontal top bar
  - Logo + name inline, nav as horizontal pill row
  - Hide heatmap widget (or move to a collapsible section / end of page)
- Ensure post content is visible within first screenful on mobile
- Adjust card grids to single column at narrow widths

## 8. Logo Optimization
**Files:** `legohat_logo.png` (replace)
- Compress the 1.4MB PNG to appropriate display size (~100px height for 2x retina)
- Convert to WebP with PNG fallback using `<picture>` element, or just serve a compressed PNG
- Target: under 30KB

---

**Execution order:** 1 → 2 → 3 → 5 → 4 → 6 → 7 → 8 (typography and color first since they affect everything else; logo last since it's independent)
