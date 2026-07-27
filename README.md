# legodud3.github.io

A custom-built static blogging engine designed for simplicity and longevity. It runs entirely on GitHub Pages without a backend database or complex build framework.

## Features

*   **Zero-Backend Architecture**: No database to maintain. The site is purely HTML, CSS, and JavaScript, making it extremely fast and secure.
*   **Browser-Based Editor**: Write and publish posts directly from browser at `../write.html` using the GitHub API - no command line needed.
*   **Automated Content Pipeline**:
    *   Posts are written in **Markdown** and stored in the `posts/` directory (organized by year).
    *   A **GitHub Action** triggers on every push, running a Python script to scan files and regenerate the `posts.json` index automatically.
*   **Smart Organization**:
    *   **Tagging System**: Supports multiple tags — Reflection, Tech, Life, Learning — each with a distinct color.
    *   **Search & Filtering**: The homepage features real-time search and tag filtering.
    *   **Pagination**: Automatically handles large archives of posts.
    *   **Surprise Me**: A button to jump to a random post for serendipitous discovery.
*   **Reading Experience**:
    *   **Side Projects Page**: A dedicated section to showcase ongoing and completed side projects with card-based layout.
    *   Client-side Markdown rendering.
    *   Previous/Next post navigation in the footer.
    *   Clean, distraction-free design with dark and light modes.
*   **Audio**: ElevenLabs-powered text-to-speech for posts, displayed via a custom LEGO-brick audio player.

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
- **LEGO Audio Player**: Brick-based progress bar with gold studs
- **Writing Consistency Heatmap**: GitHub-style contribution graph for posts
- **Project Cards**: Card grid with colored accent borders
- **Post Cards**: Card-based post list with excerpts and featured first post

## CI/CD Workflows

### Post Index (`update_posts.yml`)
- **Trigger**: Push to `posts/**/*.md`, `tags.json`, or `update_posts.py`
- **Action**: Runs `update_posts.py` to regenerate `posts.json`
- **Output**: Auto-commits updated `posts.json`

### Audio Generation (`generate_audio.yml`)
- **Trigger**: Push to `posts/**/*.md` or manual dispatch
- **Action**: Runs `generate_audio.py` using ElevenLabs API (multilingual v2 model)
- **Secrets Required**: `ELEVENLABS_API_KEY`, `ELEVENLABS_VOICE_ID`
- **Output**: Auto-commits `.mp3` files alongside posts

## Getting Started

To view the website, visit https://legodud3.github.io or simply open the `index.html` file in your web browser.

## Writing New Posts

### Option 1: Browser-Based Editor (Recommended)

1. Navigate to `https://legodud3.github.io/write.html` (or click "Write" in the navigation)
2. **First-time setup**:
   - Create a GitHub Personal Access Token (PAT):
     - Go to GitHub Settings > Developer settings > Personal access tokens > Tokens (classic)
     - Click "Generate new token (classic)"
     - Give it a name (e.g., "Blog Editor")
     - Select scope: **repo** (Full control of private repositories)
     - Click "Generate token" and copy it
   - Enter your PAT, GitHub username, and repository name
   - Optional: save only username/repository on the device for convenience
   - Click "Login & Continue"
3. **Write your post**:
   - Enter a title, select date (defaults to today), and choose a tag
   - Write your content in Markdown
   - Click "Preview" to see how it will look
   - Click "Publish Post" to commit directly to GitHub
4. GitHub Actions will automatically update the site index

### Security notes

- The editor keeps your GitHub PAT in session storage only (cleared when browser session ends).
- Username and repository can be optionally stored in local storage for convenience.

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

- [marked.js](https://marked.js.org/) — Client-side Markdown rendering (via CDN)
- [DOMPurify](https://github.com/cure53/DOMPurify) — XSS sanitization (via CDN)
- [js-yaml](https://github.com/nodeca/js-yaml) — YAML frontmatter parsing (via CDN)
- [Google Fonts](https://fonts.google.com/) — Roboto (body, headings)
