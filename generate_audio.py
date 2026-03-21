import os
import re
import sys
import argparse
import time
import requests

ELEVENLABS_API_URL = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"


def parse_front_matter(content):
    if not content.startswith("---\n"):
        return {}, content
    end = content.find("\n---", 4)
    if end == -1:
        return {}, content
    front_matter = content[4:end].strip()
    meta = {}
    for line in front_matter.splitlines():
        m = re.match(r"^([A-Za-z0-9_-]+)\s*:\s*(.*)$", line.strip())
        if m:
            meta[m.group(1).lower()] = m.group(2).strip().strip("\"'")
    return meta, content[end + 4:].strip()


def markdown_to_plain(text):
    text = re.sub(r"```[\s\S]*?```", "", text)           # fenced code blocks
    text = re.sub(r"`[^`]*`", "", text)                  # inline code
    text = re.sub(r"!\[.*?\]\(.*?\)", "", text)          # images
    text = re.sub(r"\[([^\]]+)\]\(.*?\)", r"\1", text)  # links -> link text
    text = re.sub(r"#{1,6}\s+", "", text)                # headings
    text = re.sub(r"[*_]{1,3}([^*_\n]+)[*_]{1,3}", r"\1", text)  # bold/italic
    text = re.sub(r"^\s*[-*+]\s+", "", text, flags=re.MULTILINE)  # unordered lists
    text = re.sub(r"^\s*\d+\.\s+", "", text, flags=re.MULTILINE)  # ordered lists
    text = re.sub(r"^\s*>+\s*", "", text, flags=re.MULTILINE)     # blockquotes
    text = re.sub(r"^\s*[-|=]{3,}\s*$", "", text, flags=re.MULTILINE)  # hr/tables
    text = re.sub(r"\|", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def chunk_text(text, max_chars=4800):
    sentences = re.split(r"(?<=[.!?])\s+", text)
    chunks, current = [], ""
    for s in sentences:
        if len(current) + len(s) + 1 <= max_chars:
            current = (current + " " + s).strip()
        else:
            if current:
                chunks.append(current)
            if len(s) > max_chars:
                for i in range(0, len(s), max_chars):
                    chunks.append(s[i:i + max_chars])
                current = ""
            else:
                current = s
    if current:
        chunks.append(current)
    return chunks


def tts_chunk(text, api_key, voice_id, retries=3):
    url = ELEVENLABS_API_URL.format(voice_id=voice_id)
    headers = {"xi-api-key": api_key, "Content-Type": "application/json"}
    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75},
    }
    for attempt in range(retries):
        resp = requests.post(url, json=payload, headers=headers, timeout=60)
        if resp.status_code == 200:
            return resp.content
        if resp.status_code == 429:
            wait = 2 ** attempt
            print(f"  Rate limited. Waiting {wait}s...", flush=True)
            time.sleep(wait)
        else:
            resp.raise_for_status()
    raise RuntimeError(f"TTS failed after {retries} retries")


def generate_audio(md_path, api_key, voice_id, force=False):
    mp3_path = re.sub(r"\.md$", ".mp3", md_path)
    if os.path.exists(mp3_path) and not force:
        print(f"  Skipping (already exists): {mp3_path}")
        return

    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    meta, body = parse_front_matter(content)
    title = meta.get("title", "")
    plain = markdown_to_plain(body)
    full_text = f"{title}. {plain}" if title else plain

    chunks = chunk_text(full_text)
    print(f"  {md_path}: {len(full_text)} chars -> {len(chunks)} chunk(s)")

    parts = []
    for i, chunk in enumerate(chunks):
        print(f"    Chunk {i + 1}/{len(chunks)} ({len(chunk)} chars)...", flush=True)
        parts.append(tts_chunk(chunk, api_key, voice_id))
        if i < len(chunks) - 1:
            time.sleep(0.5)

    with open(mp3_path, "wb") as f:
        for p in parts:
            f.write(p)
    print(f"  Saved: {mp3_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate TTS audio for blog posts via ElevenLabs.")
    parser.add_argument("files", nargs="*", help="Markdown file paths to process")
    parser.add_argument("--all", action="store_true", help="Process all .md files under posts/")
    parser.add_argument("--force", action="store_true", help="Overwrite existing .mp3 files")
    args = parser.parse_args()

    api_key = os.environ["ELEVENLABS_API_KEY"]
    voice_id = os.environ["ELEVENLABS_VOICE_ID"]

    targets = list(args.files)
    if args.all:
        for root, _, files in os.walk("posts"):
            for fn in files:
                if fn.endswith(".md"):
                    targets.append(os.path.join(root, fn))

    if not targets:
        print("No files to process. Pass file paths or use --all.")
        sys.exit(0)

    for path in targets:
        print(f"Processing: {path}")
        generate_audio(path, api_key, voice_id, force=args.force)
