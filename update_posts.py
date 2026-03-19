import os
import json
import re
from datetime import datetime


def parse_front_matter(content):
    if not content.startswith("---\n"):
        return {}

    end = content.find("\n---", 4)
    if end == -1:
        return {}

    front_matter = content[4:end].strip()
    meta = {}
    for line in front_matter.splitlines():
        match = re.match(r"^([A-Za-z0-9_-]+)\s*:\s*(.*)$", line.strip())
        if not match:
            continue
        key = match.group(1).strip().lower()
        value = match.group(2).strip().strip("\"'")
        meta[key] = value
    return meta


def extract_excerpt(content, max_chars=300):
    # Strip front matter
    if content.startswith("---\n"):
        end = content.find("\n---", 4)
        if end != -1:
            content = content[end + 4:]

    # Remove markdown headings, links, images, inline code, bold/italic
    content = re.sub(r"!\[.*?\]\(.*?\)", "", content)   # images
    content = re.sub(r"\[([^\]]+)\]\(.*?\)", r"\1", content)  # links
    content = re.sub(r"`[^`]*`", "", content)            # inline code
    content = re.sub(r"#{1,6}\s*", "", content)          # headings
    content = re.sub(r"[*_]{1,3}([^*_]+)[*_]{1,3}", r"\1", content)  # bold/italic
    content = re.sub(r"^\s*[-*>|]+\s*", "", content, flags=re.MULTILINE)  # list/blockquote markers

    # Collapse whitespace
    content = " ".join(content.split())

    return content[:max_chars].rstrip()


def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except (TypeError, ValueError):
        return datetime.min

def main():
    posts_dir = "posts"
    output_file = "posts.json"
    posts = []

    # Load tags from tags.json to avoid duplication
    TAG_RULES = {}
    with open("tags.json", "r", encoding="utf-8") as f:
        tags_data = json.load(f)
        for key, data in tags_data.items():
            TAG_RULES[data["name"]] = {"color": data["color"], "key": key}

    # Loop through files in posts/ directory recursively
    for root, dirs, files in os.walk(posts_dir):
        for filename in files:
            if filename.endswith(".md"):
                filepath = os.path.join(root, filename)
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()

                    meta = parse_front_matter(content)
                    title = meta.get("title", filename)
                    date = meta.get("date", "Unknown")
                    manual_tag = meta.get("tag")
                    excerpt = extract_excerpt(content)

                    tag_name = None
                    tag_key = None
                    tag_color = None

                    if manual_tag:
                        for tag, info in TAG_RULES.items():
                            if tag.lower() == manual_tag.lower():
                                tag_name = tag
                                tag_key = info["key"]
                                tag_color = info["color"]
                                break
                    
                    # Get relative path for JSON (handles subfolders)
                    rel_path = os.path.relpath(filepath, posts_dir).replace("\\", "/")
                    posts.append({
                        "title": title,
                        "date": date,
                        "filename": rel_path,
                        "tag_name": tag_name,
                        "tag_key": tag_key,
                        "tag_color": tag_color,
                        "excerpt": excerpt
                    })

    # Sort by date descending
    posts.sort(key=lambda x: parse_date(x["date"]), reverse=True)
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=2)

if __name__ == "__main__":
    main()
