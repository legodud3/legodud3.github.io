# legodud3.github.io

A custom-built static blogging engine designed for simplicity and longevity. It runs entirely on GitHub Pages without a backend database or complex build framework.

## Features

*   **Zero-Backend Architecture**: No database to maintain. The site is purely HTML, CSS, and JavaScript, making it extremely fast and secure.
*   **Markdown-first publishing**: Add a Markdown file under `posts/`, commit it, and GitHub Actions regenerates the published pages and indexes.
*   **Automated Content Pipeline**:
    *   Posts are written in **Markdown** and stored in the `posts/` directory (organized by year).
    *   A **GitHub Action** triggers on every push, running a Python script that regenerates the `posts.json` index, the `feed.xml` Atom feed, and **pre-rendered static HTML pages** for every post under `p/` (real titles, descriptions, canonical URLs, and baked-in prev/next navigation).
*   **Smart Organization**:
    *   **Search**: The homepage features real-time post search.
    *   **Pagination**: Automatically handles large archives of posts.
    *   **Surprise Me**: A button to jump to a random post for serendipitous discovery.
*   **Reading Experience**:
    *   **Side Projects Page**: A dedicated section to showcase ongoing and completed side projects with card-based layout.
    *   **Static post pages**: every post is served as a pre-rendered page at `/p/<slug>.html` — fast first paint, per-post SEO metadata, and no client-side Markdown parsing on the reader path.
    *   Previous/Next post navigation and three related-post suggestions, both baked in at build time.
    *   Clean, distraction-free design with dark and light modes.
*   **Shared Layout Module**: `layout.js` builds the left rail (brand, nav, writing heatmap) and footer from mount points, so no page duplicates that markup.

## Design System

### Typography
- Body text uses [Roboto](https://fonts.google.com/specimen/Roboto); display text uses Fraunces. The homepage has its own typography.

### Color Palette
| Token | Dark Mode | Light Mode | Usage |
|---|---|---|---|
| `--bg-color` | `#1c211f` | `#f2f0e9` | Page background |
| `--text-color` | `#f2f0e9` | `#20231f` | Body text |
| `--link-color` | `#9facff` | `#2448f2` | Hyperlinks and accent |
| `--accent-color` | `#9facff` | `#2448f2` | Brand, buttons, highlights |
| `--border-color` | `#50564e` | `#c9cbc2` | Borders & dividers |

### Key Components
- **Writing Consistency Heatmap**: GitHub-style contribution graph for posts
- **Project Cards**: Card grid with colored accent borders
- **Post List**: Compact, searchable post rows with metadata and excerpts

## CI/CD Workflows

### Post Index (`update_posts.yml`)
- **Trigger**: Push to `posts/**/*.md` or `update_posts.py`
- **Action**: Installs `markdown`, then runs `update_posts.py` to regenerate `posts.json`, `feed.xml` (Atom feed), `sitemap.xml`, and the static post pages in `p/`
- **Output**: Auto-commits updated `posts.json` + `feed.xml` + `sitemap.xml` + `p/`
- **Concurrency**: Serialized (`posts-index` group) so rapid publishes queue instead of racing
- **Note**: `p/` is fully regenerated (and wiped) on each run, so deleted or renamed posts don't leave stale pages behind
- **Note**: The Action only commits when the regenerated output actually differs. The build is byte-for-byte reproducible, so a correct checkout produces no commit at all.

### Sitemap

`sitemap.xml` is generated on every build, so new posts appear automatically. It lists the homepage, `about.html`, `side-projects.html`, and every dated post under `/p/`. Each post carries a `<lastmod>` from its front matter; the hand-maintained pages do not claim an edit date.

It's advertised in `robots.txt` and can be submitted in **Google Search Console**. `view.html` (a legacy redirect shim) and `404.html` are excluded because they are `noindex`.

### Reproducible Builds

`update_posts.py` produces identical bytes on every machine, so a local rebuild and a CI rebuild never fight each other in git. Two things make that true — please keep them intact:

- **Sorted traversal.** The post walk sorts directories and filenames, and posts are pre-sorted by filename before the date sort. `os.walk` otherwise yields *filesystem* order, which differs per machine, and the date sort is stable — so posts sharing a date could be emitted in either order and silently rewrite the index.
- **LF line endings.** All generated files are written with `newline="\n"`. Without it Python's text mode writes `\r\n` on Windows, and `.gitattributes` would have to paper over the difference.

To confirm nothing has drifted, run the build and check that git is clean:

```bash
python3 update_posts.py && git status --porcelain
```

No output means the committed artifacts match a fresh build exactly.

### Post Validation (`validate_posts.yml`)
- **Trigger**: Pull requests touching `posts/**/*.md` or `update_posts.py`
- **Action**: Runs `update_posts.py --validate`, failing on missing titles, invalid dates, misnamed files
- **Note**: `update_posts.py` is in the path filter because the validation logic lives inside it — a PR that changes the validator or the indexer must still be checked.

## Getting Started

To view the website, visit https://legodud3.github.io or simply open the `index.html` file in your web browser.

## Writing New Posts

1. Create `posts/YYYY/YYYY-MM-DD-title-slug.md` using a lowercase, hyphen-separated filename.
2. Add front matter and write the post in Markdown:
   ```yaml
   ---
   title: Your Post Title
   date: YYYY-MM-DD
   ---
   ```
3. Commit and push the file. GitHub Actions validates it and regenerates the index, feed, sitemap, and static post pages.

## Dependencies

**Build (Python, used by the GitHub Action):**
- [markdown](https://pypi.org/project/Markdown/) — renders posts to HTML for the static pages (`pip install markdown`)

**Runtime:** Chart.js is loaded from a pinned CDN only on post pages that contain charts. Google Analytics and Google Fonts are also loaded by the site.

**Fonts:**
- [Google Fonts](https://fonts.google.com/) — used for shared and homepage typography.

## Generated Files

`posts.json`, `feed.xml`, `sitemap.xml`, and everything under `p/` are **generated — never hand-edit them.** Change the Markdown in `posts/YYYY/` and re-run `update_posts.py`; the build wipes and regenerates `p/` from scratch. A post's public URL is derived from its filename (`posts/2026/2026-09-28-my-slug.md` → `/p/2026-09-28-my-slug.html`), so renaming a file changes its URL.

Post pages are pre-rendered, so `view.html` is only a small legacy redirect shim that forwards old `view.html?post=…` links to `/p/<slug>.html`.
