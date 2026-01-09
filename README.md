# legodud3.github.io

This is a simple static website built with HTML, CSS, and JavaScript. It serves as a personal blog.

## Getting Started

To view the website, visit https://legodud3.github.io or simply open the `index.html` file in your web browser.

## Adding Blog Posts

### Method 1: Manual Creation

Create a new markdown file in the `posts/` directory with the following format:

```markdown
---
title: Your Post Title
date: YYYY-MM-DD
---

# Your Post Title

Your content here...
```

### Method 2: Bulk Upload Handwritten Entries

If you have handwritten journal entries you want to convert to blog posts, use the bulk upload script:

1. Install dependencies: `pip install -r requirements.txt`
2. Get a [Gemini API key](https://aistudio.google.com/app/apikey)
3. Run: `python bulk_upload.py --input <image_directory> --api-key <your_key>`

See [BULK_UPLOAD_GUIDE.md](BULK_UPLOAD_GUIDE.md) for detailed instructions.

## File Structure

- `index.html`: The main landing page.
- `about.html`: The about page.
- `view.html`: The page for viewing individual posts.
- `style.css`: The stylesheet for the website.
- `posts.json`: A JSON file containing a list of all the blog posts.
- `posts/`: A directory containing the blog posts in Markdown format.
- `bulk_upload.py`: Script for bulk uploading handwritten journal entries using Gemini AI.
- `requirements.txt`: Python dependencies for the bulk upload script.
- `.github/workflows/update_posts.yml`: A GitHub Actions workflow to update the `posts.json` file automatically.
