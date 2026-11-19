#!/usr/bin/env python3
"""Pull and push Canvas course pages.

Usage:
  python3 canvas_pages.py pull            # download every page to pages/<slug>.html
  python3 canvas_pages.py push <slug>...  # upload edited pages/<slug>.html back to Canvas

Before each push the live page body is saved to backups/<slug>.<timestamp>.html.
Reads the API token from the `canvasapikey` environment variable.
"""
import json
import mimetypes
import os
import sys
import time
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

BASE = os.environ.get("CANVAS_BASE_URL", "https://canvas.lorainccc.edu")
COURSE = os.environ.get("CANVAS_COURSE_ID", "96040")
ROOT = Path(__file__).resolve().parent
PAGES = ROOT / "pages"
BACKUPS = ROOT / "backups"


def api(method, path, data=None):
    url = path if path.startswith("http") else f"{BASE}/api/v1{path}"
    body = urllib.parse.urlencode(data).encode() if data else None
    req = urllib.request.Request(url, data=body, method=method)
    req.add_header("Authorization", f"Bearer {os.environ['canvasapikey']}")
    with urllib.request.urlopen(req) as resp:
        return json.load(resp), resp.headers.get("Link", "")


def next_link(link_header):
    for part in link_header.split(","):
        if 'rel="next"' in part:
            return part[part.index("<") + 1 : part.index(">")]
    return None


def upload_file(course, path, folder):
    """Upload a local file to the course's Files under folder; returns the Canvas file record."""
    path = Path(path)
    content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    slot, _ = api("POST", f"/courses/{course}/files",
                  {"name": path.name, "size": path.stat().st_size, "content_type": content_type,
                   "parent_folder_path": folder, "on_duplicate": "overwrite"})
    boundary = uuid.uuid4().hex
    parts = [f'--{boundary}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode()
             for k, v in slot["upload_params"].items()]
    parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="{path.name}"\r\n'
                 f"Content-Type: {content_type}\r\n\r\n".encode() + path.read_bytes() + b"\r\n")
    body = b"".join(parts) + f"--{boundary}--\r\n".encode()
    # the upload host is a storage service; it gets the one-time upload params, not the API token
    req = urllib.request.Request(slot["upload_url"], data=body, method="POST")
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
    with urllib.request.urlopen(req) as resp:
        result = json.load(resp)
    return api("GET", f"/files/{result['id']}")[0] if "id" in result else api("GET", result["location"])[0]


def list_pages():
    pages, url = [], f"/courses/{COURSE}/pages?per_page=100"
    while url:
        batch, link = api("GET", url)
        pages.extend(batch)
        url = next_link(link)
    return pages


def pull():
    PAGES.mkdir(exist_ok=True)
    index = []
    for p in list_pages():
        page, _ = api("GET", f"/courses/{COURSE}/pages/{p['url']}")
        (PAGES / f"{p['url']}.html").write_text(page.get("body") or "")
        index.append({k: page.get(k) for k in ("url", "title", "published", "front_page", "updated_at")})
        print(f"pulled {p['url']}")
    (PAGES / "index.json").write_text(json.dumps(index, indent=2))


def push(slugs):
    BACKUPS.mkdir(exist_ok=True)
    stamp = time.strftime("%Y%m%d-%H%M%S")
    for slug in slugs:
        live, _ = api("GET", f"/courses/{COURSE}/pages/{slug}")
        (BACKUPS / f"{slug}.{stamp}.html").write_text(live.get("body") or "")
        body = (PAGES / f"{slug}.html").read_text()
        saved, _ = api("PUT", f"/courses/{COURSE}/pages/{slug}", {"wiki_page[body]": body})
        # Canvas normalizes HTML on save; keep its version so later edits start from live content
        (PAGES / f"{slug}.html").write_text(saved.get("body") or "")
        print(f"pushed {slug} (backup: backups/{slug}.{stamp}.html)")


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "pull":
        pull()
    elif len(sys.argv) >= 3 and sys.argv[1] == "push":
        push(sys.argv[2:])
    else:
        sys.exit(__doc__)
