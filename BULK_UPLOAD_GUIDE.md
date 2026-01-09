# Bulk Upload Handwritten Journal Entries

This guide explains how to bulk upload your handwritten journal entries to your blog using the Gemini AI-powered conversion script.

## Overview

The bulk upload workflow consists of three main steps:

1. **Convert**: Use Gemini AI to extract text from handwritten journal entry images and convert them to standard markdown blog posts
2. **Upload**: Save the converted markdown files to the `posts/` directory
3. **Publish**: Commit and push the changes to automatically update the blog

## Prerequisites

### 1. Get a Gemini API Key

You need a Google Gemini API key to use the conversion script:

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key and keep it secure

### 2. Install Python Dependencies

The script requires Python 3.7+ and some dependencies:

```bash
pip install -r requirements.txt
```

This will install:
- `google-generativeai`: For Gemini AI integration
- `Pillow`: For image processing

## How to Use

### Step 1: Prepare Your Images

1. Take clear photos or scans of your handwritten journal entries
2. Supported formats: JPG, JPEG, PNG, GIF, BMP, TIFF
3. Place all images in a single directory (e.g., `journal_images/`)

**Tips for best results:**
- Ensure good lighting and minimal shadows
- Keep the camera steady for clear text
- Capture the entire entry in the frame
- Higher resolution images work better

### Step 2: Run the Conversion Script

#### Option A: Using Environment Variable (Recommended)

```bash
export GEMINI_API_KEY="your-api-key-here"
./bulk_upload.sh --input journal_images/
```

Or if the wrapper doesn't work:

```bash
export GEMINI_API_KEY="your-api-key-here"
python3 -W ignore bulk_upload.py --input journal_images/
```

#### Option B: Using Command-Line Argument

```bash
./bulk_upload.sh --input journal_images/ --api-key "your-api-key-here"
```

Or:

```bash
python3 -W ignore bulk_upload.py --input journal_images/ --api-key "your-api-key-here"
```

#### Available Options

- `--input` or `-i`: Directory containing handwritten entry images (required)
- `--api-key` or `-k`: Gemini API key (or set `GEMINI_API_KEY` environment variable)
- `--output` or `-o`: Output directory for markdown files (default: `posts`)
- `--dry-run`: Process images without saving (for testing)

#### Example Commands

**Basic usage:**
```bash
./bulk_upload.sh --input ~/my_journals/2023/
```

**Test without saving:**
```bash
./bulk_upload.sh --input ~/my_journals/2023/ --dry-run
```

**Custom output directory:**
```bash
./bulk_upload.sh --input ~/my_journals/ --output my_posts/
```

### Step 3: Review the Generated Posts

The script will create markdown files in the `posts/` directory with:
- YAML frontmatter containing title and date
- Markdown-formatted content
- Proper filename (derived from the title)

Example generated file (`posts/my-first-entry.md`):

```markdown
---
title: My First Entry
date: 2023-06-15
---

# My First Entry

Today was an amazing day. I went to the park and...
```

### Step 4: Publish Your Posts

Once you're satisfied with the generated posts:

```bash
# Add all new posts
git add posts/*.md

# Commit the changes
git commit -m "Add bulk uploaded journal entries"

# Push to GitHub
git push
```

The GitHub Action will automatically:
1. Detect the new posts
2. Update `posts.json` with the new entries
3. Make them visible on your blog

## How It Works

### The Conversion Process

1. **Image Analysis**: The script loads each image using PIL (Pillow)
2. **AI Processing**: Gemini AI analyzes the handwritten text and:
   - Extracts or identifies the date
   - Creates a meaningful title based on content
   - Converts handwriting to clean, readable text
   - Formats the content as markdown
3. **Post Generation**: The script creates a markdown file with:
   - YAML frontmatter (title and date)
   - Properly formatted markdown content
4. **File Naming**: Generates a URL-friendly filename from the title

### What Gemini Extracts

The AI model looks for:
- **Date**: Extracts visible dates or uses a default
- **Title**: Identifies explicit titles or generates one from the content
- **Content**: Transcribes all handwritten text
- **Structure**: Preserves paragraphs, lists, and emphasis

### Markdown Formatting

The converted content includes:
- Headings (`#`, `##`, `###`)
- **Bold** and *italic* text
- Bulleted and numbered lists
- Paragraphs with proper spacing

## Troubleshooting

### Issue: "Error: Required packages not installed"

**Solution**: Install the dependencies:
```bash
pip install -r requirements.txt
```

### Issue: "Error: Gemini API key required"

**Solution**: Provide your API key via:
- Command line: `--api-key "your-key"`
- Environment variable: `export GEMINI_API_KEY="your-key"`

### Issue: Poor text recognition

**Solutions**:
- Use higher resolution images
- Ensure good lighting when photographing
- Check that handwriting is clearly visible
- Try retaking photos of problematic pages

### Issue: Incorrect dates

**Solution**: The script will use today's date as a fallback. You can manually edit the generated markdown files to correct dates:

```bash
# Edit the file
nano posts/my-entry.md

# Update the date in the frontmatter
date: 2023-06-15  # Change this
```

### Issue: File already exists

The script automatically handles filename conflicts by appending a timestamp. If you want to replace an existing post, delete it first:

```bash
rm posts/existing-post.md
python bulk_upload.py --input journal_images/
```

## Processing Statistics

After running, the script displays a summary:

```
Processing Summary
============================================================
Total processed: 25
Successful: 23
Failed: 2
Skipped: 0
============================================================
```

- **Total processed**: Number of images found and processed
- **Successful**: Posts successfully created
- **Failed**: Images that couldn't be converted
- **Skipped**: Images that were skipped (currently not used)

## Advanced Usage

### Batch Processing Multiple Directories

Process entries from different time periods:

```bash
python bulk_upload.py --input journals/2020/
python bulk_upload.py --input journals/2021/
python bulk_upload.py --input journals/2022/
```

### Using a Different Model

To use a different Gemini model, edit `bulk_upload.py` and change line 41:

```python
self.model = genai.GenerativeModel('gemini-1.5-pro')  # More powerful model
```

Available models:
- `gemini-1.5-flash`: Fast and efficient (default)
- `gemini-1.5-pro`: More accurate, slower

### Custom Prompt

To customize how entries are converted, edit the `_create_conversion_prompt()` method in `bulk_upload.py`.

## Security Notes

- Never commit your API key to the repository
- Use environment variables or command-line arguments
- Keep your API key secure and don't share it
- The `.gitignore` should exclude any credential files

## Cost Considerations

The Gemini API has a free tier with limitations:
- Check [Google AI pricing](https://ai.google.dev/pricing) for current rates
- The script processes one image at a time
- Processing 100 images typically uses minimal quota
- Monitor your API usage in Google AI Studio

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify your API key is valid
3. Ensure images are clear and readable
4. Check the script output for specific error messages

## Example Workflow

Here's a complete example of bulk uploading 10 years of journal entries:

```bash
# 1. Set up environment
export GEMINI_API_KEY="your-api-key-here"

# 2. Install dependencies
pip install -r requirements.txt

# 3. Test with a few images first
python bulk_upload.py --input sample_journals/ --dry-run

# 4. Process all entries
python bulk_upload.py --input all_journals/

# 5. Review generated posts
ls -l posts/

# 6. Make any manual corrections
nano posts/entry-with-issue.md

# 7. Publish to blog
git add posts/*.md
git commit -m "Add 10 years of journal entries"
git push

# 8. Wait for GitHub Action to complete (~30 seconds)
# 9. Visit your blog to see the new posts!
```

## Files Overview

- `bulk_upload.py`: Main conversion script
- `requirements.txt`: Python dependencies
- `BULK_UPLOAD_GUIDE.md`: This documentation
- `posts/`: Directory where converted posts are saved
- `.github/workflows/update_posts.yml`: Auto-updates posts.json

## Next Steps

After bulk uploading:
1. Review posts on your blog
2. Edit any posts that need corrections
3. Add images or multimedia to posts if desired
4. Update post titles or dates as needed
5. Continue adding new posts using the same workflow!
