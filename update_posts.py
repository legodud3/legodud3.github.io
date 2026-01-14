import os
import json
import re
import sys

def main():
    # Load tags
    try:
        with open("tags.json", "r", encoding="utf-8") as f:
            tags_data = json.load(f)
    except FileNotFoundError:
        print("tags.json not found.")
        sys.exit(1)

    posts = []
    posts_dir = "posts"

    # Loop through files in posts/ directory recursively
    for root, dirs, files in os.walk(posts_dir):
        for filename in files:
            if filename.endswith(".md"):
                filepath = os.path.join(root, filename)
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()

                    # Extract title, date, tag using Regex
                    # Note: We need to handle potential quotes and whitespace
                    title_match = re.search(r"^title:\s*(.*)", content, re.MULTILINE)
                    date_match = re.search(r"^date:\s*(.*)", content, re.MULTILINE)
                    tag_match = re.search(r"^tag:\s*(.*)", content, re.MULTILINE)

                    # Strip quotes safely
                    title = title_match.group(1).strip().strip('"\'').strip() if title_match else filename
                    date = date_match.group(1).strip().strip('"\'').strip() if date_match else "Unknown"
                    tag_key = tag_match.group(1).strip().strip('"\'').strip() if tag_match else None

                    # Resolve tag info
                    tag_name = None
                    tag_color = None

                    if tag_key:
                        # Case insensitive lookup
                        if tag_key in tags_data:
                            tag_info = tags_data[tag_key]
                            tag_name = tag_info["name"]
                            tag_color = tag_info["color"]
                        elif tag_key.lower() in tags_data:
                             tag_info = tags_data[tag_key.lower()]
                             tag_name = tag_info["name"]
                             tag_color = tag_info["color"]
                             tag_key = tag_key.lower() # Normalize key
                        else:
                            # Tag specified but not found in tags.json
                            print(f"Warning: Tag '{tag_key}' in {filename} not found in tags.json")
                            tag_key = None # Treat as untagged

                    # Get relative path for JSON (handles subfolders)
                    rel_path = os.path.relpath(filepath, posts_dir).replace("\\", "/")

                    post_data = {
                        "title": title,
                        "date": date,
                        "filename": rel_path
                    }

                    if tag_key:
                        post_data["tag_key"] = tag_key
                        post_data["tag_name"] = tag_name
                        post_data["tag_color"] = tag_color

                    posts.append(post_data)

    # Sort by date descending
    posts.sort(key=lambda x: x["date"], reverse=True)

    with open("posts.json", "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=2)

    print(f"Generated posts.json with {len(posts)} posts.")

if __name__ == "__main__":
    main()
