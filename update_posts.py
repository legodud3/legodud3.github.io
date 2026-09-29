import json
import os
import re
import sys
from datetime import datetime, timezone
from urllib.parse import quote
from xml.sax.saxutils import escape

SITE_URL = "https://legodud3.github.io"
SITE_TITLE = "Chinmay Deo"
SITE_DESCRIPTION = "Personal blog of Chinmay Deo — short posts on learning, tech, and life."
FEED_FILE = "feed.xml"
FEED_ENTRIES = 20
POST_PATH_RE = re.compile(r"^\d{4}/\d{4}-\d{2}-\d{2}-.+\.md$")


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
        value = match.group(2).strip()
        # Unquote YAML-style quoted scalars — write.html emits quoted titles so
        # titles containing ':' or '#' survive every parser in this repo.
        if len(value) >= 2 and value.startswith('"') and value.endswith('"'):
            value = value[1:-1].replace('\\"', '"').replace("\\\\", "\\")
        elif len(value) >= 2 and value.startswith("'") and value.endswith("'"):
            value = value[1:-1].replace("''", "'")
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


def iso_date(date_str):
    return parse_date(date_str).replace(tzinfo=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def validate_post(rel_path, meta, tag_name):
    """Return a list of metadata problems for a post (empty list = valid)."""
    problems = []
    if not POST_PATH_RE.match(rel_path):
        problems.append(f"{rel_path}: path should be posts/YYYY/YYYY-MM-DD-title-slug.md")
    if parse_date(meta.get("date")) == datetime.min:
        problems.append(f"{rel_path}: missing or invalid date (expected YYYY-MM-DD)")
    if not meta.get("title"):
        problems.append(f"{rel_path}: missing title")
    if meta.get("tag") and not tag_name:
        problems.append(f"{rel_path}: unknown tag '{meta['tag']}' (not in tags.json)")
    return problems


def build_feed(posts):
    """Build an Atom feed (feed.xml) from the newest dated posts."""
    entries = []
    for post in posts:
        if parse_date(post["date"]) == datetime.min:
            continue  # undated posts can't be ordered in a feed
        link = f'{SITE_URL}/view.html?post={quote(post["filename"])}'
        category = f'    <category term="{escape(post["tag_name"])}" />\n' if post["tag_name"] else ""
        entries.append(
            f'  <entry>\n'
            f'    <title>{escape(post["title"])}</title>\n'
            f'    <link href="{escape(link)}" rel="alternate" />\n'
            f'    <id>{escape(link)}</id>\n'
            f'    <published>{iso_date(post["date"])}</published>\n'
            f'    <updated>{iso_date(post["date"])}</updated>\n'
            f'{category}'
            f'    <summary>{escape(post["excerpt"])}</summary>\n'
            f'  </entry>'
        )
        if len(entries) >= FEED_ENTRIES:
            break

    dated = [p for p in posts if parse_date(p["date"]) != datetime.min]
    feed_updated = iso_date(dated[0]["date"]) if dated else datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    return (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<feed xmlns="http://www.w3.org/2005/Atom">\n'
        f'  <title>{escape(SITE_TITLE)}</title>\n'
        f'  <subtitle>{escape(SITE_DESCRIPTION)}</subtitle>\n'
        f'  <link href="{SITE_URL}/" rel="alternate" />\n'
        f'  <link href="{SITE_URL}/{FEED_FILE}" rel="self" />\n'
        f'  <id>{SITE_URL}/</id>\n'
        f'  <updated>{feed_updated}</updated>\n'
        + "\n".join(entries)
        + '\n</feed>\n'
    )


def main(validate_only=False):
    posts_dir = "posts"
    output_file = "posts.json"
    posts = []
    problems = []

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
                problems.extend(validate_post(rel_path, meta, tag_name))

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

    for problem in problems:
        print(f"WARNING: {problem}", file=sys.stderr)

    # --validate mode: report metadata problems and exit non-zero (used by CI)
    if validate_only:
        if problems:
            print(f"{len(problems)} problem(s) found.", file=sys.stderr)
            sys.exit(1)
        print(f"All {len(posts)} posts valid.")
        return

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=2)

    with open(FEED_FILE, "w", encoding="utf-8") as f:
        f.write(build_feed(posts))

    print(f"Wrote {output_file} ({len(posts)} posts) and {FEED_FILE}.")


if __name__ == "__main__":
    main(validate_only="--validate" in sys.argv)
