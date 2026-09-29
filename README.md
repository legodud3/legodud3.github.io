# legodud3.github.io

A custom-built static blogging engine designed for simplicity and longevity. It runs entirely on GitHub Pages without a backend database or complex build framework.

## Features

*   **Zero-Backend Architecture**: No database to maintain. The site is purely HTML, CSS, and JavaScript, making it extremely fast and secure.
*   **Browser-Based Editor**: Write, format, preview, and publish posts directly from `write.html` using the GitHub API—no command line needed.
*   **Automated Content Pipeline**:
    *   Posts are written in **Markdown** and stored in the `posts/` directory (organized by year).
    *   A **GitHub Action** triggers on every push, running a Python script that regenerates the `posts.json` index, the `feed.xml` Atom feed, and **pre-rendered static HTML pages** for every post under `p/` (real titles, descriptions, canonical URLs, and baked-in prev/next navigation).
*   **Smart Organization**:
    *   **Tagging System**: Supports multiple tags — Reflection, Tech, Life, Learning — each with a distinct color.
    *   **Search & Filtering**: The homepage features real-time search and tag filtering.
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
- **All text**: [Roboto](https://fonts.google.com/specimen/Roboto) — a clean, readable sans-serif

### Color Palette
| Token | Dark Mode | Light Mode | Usage |
|---|---|---|---|
| `--bg-color` | `#1a1a1a` | `#ffffff` | Page background |
| `--text-color` | `#e0e0e0` | `#1a1a1a` | Body text |
| `--link-color` | `#4da6ff` | `#0066cc` | Hyperlinks |
| `--accent-color` | `#FFD700` (gold) | `#DAA520` | Brand, buttons, highlights |
| `--border-color` | `#333` | `#e0e0e0` | Borders & dividers |

### Tag Colors
| Tag | Color |
|---|---|
| Reflection | `#27ae60` (green) |
| Tech | `#e67e22` (orange) |
| Life | `#2980b9` (blue) |
| Learning | `#8e44ad` (purple) |

### Key Components
- **Writing Consistency Heatmap**: GitHub-style contribution graph for posts
- **Project Cards**: Card grid with colored accent borders
- **Post List**: Compact, searchable post rows with metadata and excerpts

## CI/CD Workflows

### Post Index (`update_posts.yml`)
- **Trigger**: Push to `posts/**/*.md`, `tags.json`, or `update_posts.py`
- **Action**: Installs `markdown`, then runs `update_posts.py` to regenerate `posts.json`, `feed.xml` (Atom feed), and the static post pages in `p/`
- **Output**: Auto-commits updated `posts.json` + `feed.xml` + `p/`
- **Concurrency**: Serialized (`posts-index` group) so rapid publishes queue instead of racing
- **Note**: `p/` is fully regenerated (and wiped) on each run, so deleted or renamed posts don't leave stale pages behind
- **Note**: The Action only commits when the regenerated output actually differs. The build is byte-for-byte reproducible, so a correct checkout produces no commit at all.

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
- **Trigger**: Pull requests touching `posts/**/*.md`, `tags.json`, or `update_posts.py`
- **Action**: Runs `update_posts.py --validate`, failing on missing titles, invalid dates, unknown tags, or misnamed files
- **Note**: `update_posts.py` is in the path filter because the validation logic lives inside it — a PR that changes the validator or the indexer must still be checked.

## Getting Started

To view the website, visit https://legodud3.github.io or simply open the `index.html` file in your web browser.

## Writing New Posts

### Option 1: Browser-Based Editor (Recommended)

1. Navigate to `https://legodud3.github.io/write.html` or use “Open the writing desk” in the site footer.
2. **First-time setup**:
   - Create a fine-grained GitHub Personal Access Token limited to `legodud3.github.io`.
   - Grant repository permission **Contents: Read and write**.
   - Enter the token; the owner and repository are fixed by the editor.
   - Click "Login & Continue"
3. **Write your post**:
   - Enter a title, select date (defaults to today), and choose a tag
   - Write in plain Markdown in the text area — the formatting toolbar and `Ctrl`/`Cmd` + `B`/`I`/`K` shortcuts insert Markdown syntax rather than rich HTML, so what you paste in is exactly what gets committed
   - Click "Preview" to see how it will look
   - Click "Publish Post" to commit directly to GitHub
4. GitHub Actions will automatically update the site index

### Security notes

- The editor keeps your GitHub PAT in session storage only (cleared when browser session ends).
- The token is sent only to GitHub's API and is never persisted in local storage.

### Option 2: Manual File Creation

1. Create a new `.md` file in `posts/YYYY/` (where YYYY is the current year)
2. Name it using the format: `YYYY-MM-DD-title-slug.md`
3. Add front matter at the top:
   ```yaml
   ---
   title: Your Post Title
   date: YYYY-MM-DD
   tag: Reflection
   ---
   ```
4. Write your content in Markdown below the front matter
5. Commit and push to GitHub

## Dependencies

**Build (Python, used by the GitHub Action):**
- [markdown](https://pypi.org/project/Markdown/) — renders posts to HTML for the static pages (`pip install markdown`)

**Runtime (CDN, only loaded by the browser-based editor `write.html` for its preview):**
- [marked.js](https://marked.js.org/) `18.0.14` — Markdown rendering (via CDN, version-pinned with an SRI `integrity` hash)
- [DOMPurify](https://github.com/cure53/DOMPurify) `3.2.6` — XSS sanitization (via CDN, version-pinned with an SRI `integrity` hash)

The reader path (`index.html` and every page under `p/`) loads **no third-party JavaScript at all** — posts are pre-rendered, so `marked`, `DOMPurify` and `js-yaml` are no longer needed there.

**Fonts:**
- [Google Fonts](https://fonts.google.com/) — Roboto (body, headings)

## Generated Files

`posts.json`, `feed.xml`, and everything under `p/` are **generated — never hand-edit them.** Change the Markdown in `posts/YYYY/` (or `tags.json`) and re-run `update_posts.py`; the build wipes and regenerates `p/` from scratch. A post's public URL is derived from its filename (`posts/2026/2026-09-28-my-slug.md` → `/p/2026-09-28-my-slug.html`), so renaming a file changes its URL.

Post pages are pre-rendered, so `view.html` is only a small legacy redirect shim that forwards old `view.html?post=…` links to `/p/<slug>.html`.
