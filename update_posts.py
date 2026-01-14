import os
import json
import re

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
                    
                    # Extract title and date using Regex
                    title_match = re.search(r"^title:\s*(.*)", content, re.MULTILINE)
                    date_match = re.search(r"^date:\s*(.*)", content, re.MULTILINE)
                    tag_match = re.search(r"^tag:\s*(.*)", content, re.MULTILINE)
                    
                    title = title_match.group(1).strip().strip('"\'').strip() if title_match else filename
                    date = date_match.group(1).strip().strip('"\'').strip() if date_match else "Unknown"
                    manual_tag = tag_match.group(1).strip().strip('"\'').strip() if tag_match else None

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
                    posts.append({"title": title, "date": date, "filename": rel_path, "tag_name": tag_name, "tag_key": tag_key, "tag_color": tag_color})

    # Sort by date descending
    posts.sort(key=lambda x: x["date"], reverse=True)
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=2)

if __name__ == "__main__":
    main()