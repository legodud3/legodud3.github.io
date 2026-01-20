# legodud3.github.io

This is a custom-built static blogging engine designed for simplicity and longevity. It runs entirely on GitHub Pages without a backend database or complex build framework.

## Features

*   **Zero-Backend Architecture**: No database to maintain. The site is purely HTML, CSS, and JavaScript, making it extremely fast and secure.
*   **Browser-Based Editor**: Write and publish posts directly from your browser at `/write.html` using the GitHub API - no command line needed!
*   **Automated Content Pipeline**:
    *   Posts are written in **Markdown** and stored in the `posts/` directory (organized by year).
    *   A **GitHub Action** triggers on every push, running a Python script to scan files and regenerate the `posts.json` index automatically.
*   **Smart Organization**:
    *   **Tagging System**: Created but only 1 tag for now "Reflection". More to be added as content expands.
    *   **Search & Filtering**: The homepage features real-time search and tag filtering.
    *   **Pagination**: Automatically handles large archives of posts.
    *   **Surprise Me**: A button to jump to a random post for serendipitous discovery.
*   **Reading Experience**:
    *   **Side Projects Page**: A dedicated section to showcase ongoing and completed side projects.
    *   Client-side Markdown rendering.
    *   Previous/Next post navigation in the footer.
    *   Clean, distraction-free design with dark and light modes

## Getting Started

To view the website, visit https://legodud3.github.io or simply open the `index.html` file in your web browser.

## Writing New Posts

### Option 1: Browser-Based Editor (Recommended)

1. Navigate to `https://legodud3.github.io/write.html` (or click "✍️ Write" in the navigation)
2. **First-time setup**:
   - Create a GitHub Personal Access Token (PAT):
     - Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
     - Click "Generate new token (classic)"
     - Give it a name (e.g., "Blog Editor")
     - Select scope: **repo** (Full control of private repositories)
     - Click "Generate token" and copy it
   - Enter your PAT, GitHub username, and repository name
   - Click "Login & Continue"
3. **Write your post**:
   - Enter a title, select date (defaults to today), and choose a tag
   - Write your content in Markdown
   - Click "Preview" to see how it will look
   - Click "Publish Post" to commit directly to GitHub
4. GitHub Actions will automatically update the site index

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
