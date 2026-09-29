import json
import os
import re
import sys
from datetime import datetime, timezone
from html import escape as html_escape
from urllib.parse import quote as url_quote
from xml.sax.saxutils import escape as xml_escape

SITE_URL = "https://legodud3.github.io"
SITE_TITLE = "Chinmay Deo"
SITE_AUTHOR = "Chinmay Deo"
# Static share card (1200x630) used for og:image / twitter:image on every page.
OG_IMAGE_URL = f"{SITE_URL}/og-image.png"
OG_IMAGE_ALT = "Chinmay Deo — personal blog"
SITE_DESCRIPTION = "Personal blog of Chinmay Deo — short posts on learning, tech, and life."
FEED_FILE = "feed.xml"
FEED_ENTRIES = 20
SITEMAP_FILE = "sitemap.xml"
PAGES_DIR = "p"
# Hand-maintained pages that belong in the sitemap alongside the generated posts.
STATIC_PAGES = ["", "about.html", "side-projects.html"]
POST_PATH_RE = re.compile(r"^\d{4}/\d{4}-\d{2}-\d{2}-.+\.md$")
# Filenames become public URLs (/p/<name>.html), so keep them slug-safe.
SLUG_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-[a-z0-9]+(-[a-z0-9]+)*\.md$")


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


def strip_front_matter(content):
    """Return the markdown body without the front matter block."""
    if content.startswith("---\n"):
        end = content.find("\n---", 4)
        if end != -1:
            return content[end + 4:].strip()
    return content.strip()


def post_url(rel_path):
    """Root-relative URL of the generated static page for a post."""
    slug = os.path.basename(rel_path)[:-3]  # strip .md
    return f"/{PAGES_DIR}/{slug}.html"


def extract_excerpt(content, max_chars=300):
    # Strip front matter
    content = strip_front_matter(content)

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
    if not SLUG_RE.match(os.path.basename(rel_path)):
        problems.append(
            f"{rel_path}: filename should be YYYY-MM-DD-lowercase-slug.md "
            "(no spaces, uppercase, or ' copy' suffixes) — it becomes the post URL"
        )
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
        link = f'{SITE_URL}{post["url"]}'
        category = f'    <category term="{xml_escape(post["tag_name"])}" />\n' if post["tag_name"] else ""
        entries.append(
            f'  <entry>\n'
            f'    <title>{xml_escape(post["title"])}</title>\n'
            f'    <link href="{xml_escape(link)}" rel="alternate" />\n'
            f'    <id>{xml_escape(link)}</id>\n'
            f'    <published>{iso_date(post["date"])}</published>\n'
            f'    <updated>{iso_date(post["date"])}</updated>\n'
            f'{category}'
            f'    <summary>{xml_escape(post["excerpt"])}</summary>\n'
            f'  </entry>'
        )
        if len(entries) >= FEED_ENTRIES:
            break

    dated = [p for p in posts if parse_date(p["date"]) != datetime.min]
    feed_updated = iso_date(dated[0]["date"]) if dated else datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    return (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<feed xmlns="http://www.w3.org/2005/Atom">\n'
        f'  <title>{xml_escape(SITE_TITLE)}</title>\n'
        f'  <subtitle>{xml_escape(SITE_DESCRIPTION)}</subtitle>\n'
        f'  <link href="{SITE_URL}/" rel="alternate" />\n'
        f'  <link href="{SITE_URL}/{FEED_FILE}" rel="self" />\n'
        f'  <id>{SITE_URL}/</id>\n'
        f'  <updated>{feed_updated}</updated>\n'
        + "\n".join(entries)
        + '\n</feed>\n'
    )


def build_sitemap(posts):
    """Build a sitemap.xml listing every indexable page.

    Covers the hand-maintained pages plus every post's static page, so crawlers
    (and agents) get a machine-readable index of the whole site. Undated posts are
    skipped, matching build_feed. Output is a pure function of the posts, so the
    build stays reproducible: no build timestamp is embedded anywhere.
    """
    urls = []
    for path in STATIC_PAGES:
        # No <lastmod> for hand-maintained pages — we have no reliable edit date,
        # and inventing one (e.g. the newest post date) would be misleading.
        urls.append(f"  <url>\n    <loc>{xml_escape(SITE_URL + '/' + path)}</loc>\n  </url>")

    for post in posts:
        if parse_date(post["date"]) == datetime.min:
            continue  # undated posts have no meaningful lastmod
        loc = f'{SITE_URL}{post["url"]}'
        # Date-only (W3C Datetime permits it). A post's front matter carries no
        # time component, so emitting T00:00:00Z would invent precision we don't have.
        lastmod = parse_date(post["date"]).strftime("%Y-%m-%d")
        urls.append(
            f"  <url>\n"
            f"    <loc>{xml_escape(loc)}</loc>\n"
            f"    <lastmod>{lastmod}</lastmod>\n"
            f"  </url>"
        )

    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls)
        + "\n</urlset>\n"
    )


def render_markdown(text):
    # Imported lazily so `--validate` runs need no third-party packages.
    # Requires: pip install markdown
    import markdown

    return markdown.markdown(text, extensions=["fenced_code", "tables"])


def significant_words(text):
    """Words longer than 4 chars, used for excerpt-overlap scoring."""
    return {word for word in re.sub(r"[^a-z0-9\s]", " ", (text or "").lower()).split() if len(word) > 4}


def find_related_posts(posts, current, count=3):
    """Related posts: same tag first, then excerpt keyword overlap.
    Mirrors the heuristic the old client-side reader used."""
    current_words = significant_words(current.get("excerpt"))
    scored = []
    for post in posts:
        if post["filename"] == current["filename"]:
            continue
        score = 0
        if post.get("tag_key") and post["tag_key"] == current.get("tag_key"):
            score += 3
        if current_words:
            score += len(current_words & significant_words(post.get("excerpt")))
        scored.append((score, post))

    # Stable sort keeps newest-first order for ties.
    scored.sort(key=lambda item: item[0], reverse=True)
    ranked = [post for _, post in scored]
    if scored and all(score == 0 for score, _ in scored):
        return ranked[:count]  # nothing in common — fall back to newest posts
    matched = [post for score, post in scored if score > 0]
    return (matched or ranked)[:count]


def build_related_html(related):
    if not related:
        return ""
    cards = []
    for post in related:
        tag_html = ""
        if post["tag_name"] and post["tag_key"]:
            tag_html = (
                f' <span class="post-tag tag-{post["tag_key"]}">'
                f'[{html_escape(post["tag_name"])}]</span>'
            )
        excerpt = html_escape((post["excerpt"] or "")[:100].rstrip() + "…") if post["excerpt"] else ""
        cards.append(
            f'                    <a class="related-post-card" href="{post["url"]}">\n'
            f'                        <div class="related-post-title">{html_escape(post["title"])}</div>\n'
            f'                        <div><span class="post-date">[{html_escape(post["date"])}]</span>{tag_html}</div>\n'
            + (f'                        <div class="related-post-excerpt">{excerpt}</div>\n' if excerpt else "")
            + '                    </a>'
        )
    return (
        '\n            <section class="related-posts-section" aria-label="Related posts">\n'
        '                <h2 class="related-posts-heading">Related Posts</h2>\n'
        '                <div class="related-posts-grid">\n'
        + "\n".join(cards)
        + '\n                </div>\n'
        '            </section>\n'
    )


# Copy-link behavior for the static share row on post pages. Kept as a constant
# so the page template stays a plain f-string without doubled braces.
SHARE_ROW_SCRIPT = """
    <script>
    (function () {
        var btn = document.querySelector('.share-copy');
        if (!btn) { return; }
        btn.addEventListener('click', function () {
            var url = btn.getAttribute('data-copy-url');
            function done() {
                btn.textContent = 'Copied!';
                setTimeout(function () { btn.textContent = 'Copy link'; }, 2000);
            }
            if (navigator.clipboard && navigator.clipboard.writeText) {
                navigator.clipboard.writeText(url).then(done, done);
            } else {
                var ta = document.createElement('textarea');
                ta.value = url;
                document.body.appendChild(ta);
                ta.select();
                try { document.execCommand('copy'); } catch (e) {}
                document.body.removeChild(ta);
                done();
            }
        });
    })();
    </script>
"""


def build_post_page(post, posts):
    """Render a fully static HTML page for a post (real <title>, OG tags,
    canonical URL, JSON-LD, baked-in prev/next nav and related posts). Rail and
    footer come from layout.js at view time, same as the hand-written pages."""
    title = html_escape(post["title"])
    description = html_escape((post["excerpt"] or "")[:200])
    absolute_url = f'{SITE_URL}{post["url"]}'

    # URL-encoded parts for the static share links (safe to splice into hrefs).
    share_url = url_quote(absolute_url, safe="")
    share_text = url_quote(post["title"], safe="")

    # Article structured data. "<" is escaped as a JSON unicode escape so post
    # titles (untrusted input) can never break out of the <script> context.
    json_ld = json.dumps({
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": post["title"][:110],
        "datePublished": iso_date(post["date"]),
        "url": absolute_url,
        "mainEntityOfPage": absolute_url,
        "image": OG_IMAGE_URL,
        "author": {"@type": "Person", "name": SITE_AUTHOR, "url": f"{SITE_URL}/about.html"},
        "publisher": {"@type": "Person", "name": SITE_AUTHOR},
    }, separators=(",", ":"), ensure_ascii=False).replace("<", "\\u003c")

    index = posts.index(post)
    newer_post = posts[index - 1] if index > 0 else None
    older_post = posts[index + 1] if index + 1 < len(posts) else None

    tag_html = ""
    if post["tag_name"] and post["tag_key"]:
        tag_html = f'<span class="post-tag tag-{post["tag_key"]}">[{html_escape(post["tag_name"])}]</span>\n                '

    if newer_post:
        newer_link = f'<a class="visible" href="{newer_post["url"]}">← {html_escape(newer_post["title"])}</a>'
    else:
        newer_link = "<span></span>"
    if older_post:
        older_link = f'<a class="visible" href="{older_post["url"]}">{html_escape(older_post["title"])} →</a>'
    else:
        older_link = "<span></span>"

    content_html = render_markdown(post["_body"])
    related_html = build_related_html(find_related_posts(posts, post))

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Chinmay Deo</title>
    <meta name="description" content="{description}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="{absolute_url}">
    <meta property="article:published_time" content="{iso_date(post["date"])}">
    <meta property="og:image" content="{OG_IMAGE_URL}">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:image:alt" content="{OG_IMAGE_ALT}">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{description}">
    <meta name="twitter:image" content="{OG_IMAGE_URL}">
    <link rel="canonical" href="{absolute_url}">
    <script type="application/ld+json">{json_ld}</script>
    <script>if (localStorage.getItem('theme') === 'light') document.documentElement.classList.add('light-mode');</script>
    <link rel="icon" type="image/png" href="/legohat_logo.png">
    <link rel="alternate" type="application/atom+xml" title="Chinmay Deo — Writing" href="/feed.xml">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,400;0,500;0,700;1,400&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/style.css">
</head>
<body data-page="post">
    <div class="app-shell">
        <aside class="left-rail" data-layout-rail></aside>

        <main class="main-panel">
            <header class="page-header page-header-slim">
                <a href="/index.html" class="back-link" style="margin: 0;">← Back to Posts</a>
            </header>

            <article class="markdown-body">
                <h1 class="post-reader-title">{title}</h1>
                <div class="post-meta">{tag_html}[{html_escape(post["date"])}]</div>
{content_html}
            </article>

            <div class="share-row" aria-label="Share this post">
                <span class="share-label">Share</span>
                <a class="share-link" href="https://news.ycombinator.com/submitlink?u={share_url}&amp;t={share_text}" target="_blank" rel="noopener noreferrer">Hacker News</a>
                <a class="share-link" href="https://twitter.com/intent/tweet?url={share_url}&amp;text={share_text}" target="_blank" rel="noopener noreferrer">X</a>
                <a class="share-link" href="https://www.linkedin.com/sharing/share-offsite/?url={share_url}" target="_blank" rel="noopener noreferrer">LinkedIn</a>
                <button type="button" class="share-link share-copy" data-copy-url="{absolute_url}">Copy link</button>
            </div>

            <div class="post-nav">
                {newer_link}
                {older_link}
            </div>
{related_html}
            <footer class="site-footer" data-layout-footer></footer>
        </main>
    </div>

    <script src="/layout.js"></script>
    <script src="/monthly-heatmap.js"></script>
    <script src="/theme-toggle.js"></script>{SHARE_ROW_SCRIPT}
</body>
</html>
"""


def build_post_pages(posts):
    """(Re)generate the static per-post pages under PAGES_DIR. The directory
    is wiped first so deleted/renamed posts don't linger."""
    os.makedirs(PAGES_DIR, exist_ok=True)
    for existing in os.listdir(PAGES_DIR):
        if existing.endswith(".html"):
            os.remove(os.path.join(PAGES_DIR, existing))

    for post in posts:
        slug = os.path.basename(post["filename"])[:-3]
        page_path = os.path.join(PAGES_DIR, f"{slug}.html")
        # newline="\n" keeps output byte-identical on Windows and Linux: without
        # it Python's text mode translates \n to \r\n on Windows, so a local
        # rebuild would rewrite every artifact with different bytes.
        with open(page_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(build_post_page(post, posts))

    return len(posts)


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

    # Loop through files in posts/ directory recursively.
    # os.walk yields entries in filesystem order, which varies between machines,
    # so sort dirs/files to keep the build byte-for-byte reproducible.
    for root, dirs, files in os.walk(posts_dir):
        dirs.sort()
        for filename in sorted(files):
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
                    "url": post_url(rel_path),
                    "tag_name": tag_name,
                    "tag_key": tag_key,
                    "tag_color": tag_color,
                    "excerpt": excerpt,
                    "_body": strip_front_matter(content)  # internal: used for static pages, stripped from posts.json
                })

    # Sort by date descending. Sort by filename first so posts sharing a date keep a
    # stable, reproducible order (the date sort is stable and preserves it).
    posts.sort(key=lambda x: x["filename"])
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

    # Internal keys (prefixed with _) never reach posts.json
    serializable = [{k: v for k, v in post.items() if not k.startswith("_")} for post in posts]
    with open(output_file, "w", encoding="utf-8", newline="\n") as f:
        json.dump(serializable, f, indent=2)

    with open(FEED_FILE, "w", encoding="utf-8", newline="\n") as f:
        f.write(build_feed(posts))

    with open(SITEMAP_FILE, "w", encoding="utf-8", newline="\n") as f:
        f.write(build_sitemap(posts))

    page_count = build_post_pages(posts)

    print(
        f"Wrote {output_file} ({len(posts)} posts), {FEED_FILE}, {SITEMAP_FILE}, "
        f"and {page_count} static pages in {PAGES_DIR}/."
    )


if __name__ == "__main__":
    main(validate_only="--validate" in sys.argv)
