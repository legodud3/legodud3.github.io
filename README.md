# legodud3.github.io

This is a custom-built static blogging engine designed for simplicity and longevity. It runs entirely on GitHub Pages without a backend database or complex build framework.

## Features

*   **Zero-Backend Architecture**: No database to maintain. The site is purely HTML, CSS, and JavaScript, making it extremely fast and secure.
*   **Automated Content Pipeline**:
    *   Posts are written in **Markdown** and stored in the `posts/` directory (organized by year).
    *   A **GitHub Action** triggers on every push, running a Python script to scan files and regenerate the `posts.json` index automatically.
*   **Smart Organization**:
    *   **Tagging System**: Created but only 1 tag for now "Reflection". More to be added as content expands.
    *   **Search & Filtering**: The homepage features real-time search and tag filtering.
    *   **Pagination**: Automatically handles large archives of posts.
*   **Reading Experience**:
    *   Client-side Markdown rendering.
    *   Previous/Next post navigation in the footer.
    *   Clean, distraction-free dark mode design.

## Getting Started

To view the website, visit https://legodud3.github.io or simply open the `index.html` file in your web browser.
