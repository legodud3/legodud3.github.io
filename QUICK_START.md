# Quick Start: Bulk Upload Handwritten Entries

This is a quick reference for the bulk upload workflow. See [BULK_UPLOAD_GUIDE.md](BULK_UPLOAD_GUIDE.md) for complete documentation.

## Prerequisites

1. Get a Gemini API key: https://aistudio.google.com/app/apikey
2. Install dependencies: `pip install -r requirements.txt`

## Three Simple Steps

### 1. Prepare Images

Place photos/scans of your handwritten entries in a directory:
```
my_journals/
  ├── entry1.jpg
  ├── entry2.jpg
  └── entry3.jpg
```

### 2. Convert & Upload

```bash
export GEMINI_API_KEY="your-api-key-here"
./bulk_upload.sh --input my_journals/
```

### 3. Publish

```bash
git add posts/*.md
git commit -m "Add journal entries"
git push
```

Done! Your posts will appear on your blog in ~30 seconds.

## Example Output

Input: Photo of handwritten entry with "June 15, 2023" and "Today was amazing..."

Output: `posts/today-was-amazing.md`
```markdown
---
title: Today Was Amazing
date: 2023-06-15
---

# Today Was Amazing

Today was an amazing day. I went to the park and...
```

## Troubleshooting

**Script not working?** Try:
```bash
python3 -W ignore bulk_upload.py --input my_journals/
```

**Need help?** See the full guide: [BULK_UPLOAD_GUIDE.md](BULK_UPLOAD_GUIDE.md)
