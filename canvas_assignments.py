#!/usr/bin/env python3
"""Read Canvas assignments and download student submissions for review.

Usage:
  python3 canvas_assignments.py list                 # assignments with submission counts
  python3 canvas_assignments.py show <assignment_id> # instructions, points, rubric
  python3 canvas_assignments.py pull <assignment_id> # download submissions and extract text

`pull` writes to submissions/<assignment_id>/ (git-ignored: student work is FERPA-protected):
  assignment.md            instructions and rubric as text
  <student>/<files>        original uploads
  <student>/<file>.txt     text extracted from .docx, .pdf, and plain-text uploads
  index.json               student, status, late flag, score, and files for each submission

Reads the API token from the `canvasapikey` environment variable.
"""
import html
import json
import re
import subprocess
import sys
import urllib.request
import zipfile
from pathlib import Path

from canvas_pages import COURSE, ROOT, api, next_link

OUT = ROOT / "submissions"
TEXT_EXTS = {"txt", "csv", "sql", "r", "py", "md"}
MAX_DOCX_XML = 50 * 1024 * 1024  # refuse oversized document.xml (zip bomb guard)


def get_all(path):
    items, url = [], path
    while url:
        batch, link = api("GET", url)
        items.extend(batch)
        url = next_link(link)
    return items


def html_to_text(body):
    body = re.sub(r"(?i)<br\s*/?>|</p>|</li>|</h\d>|</tr>", "\n", body or "")
    body = re.sub(r"(?i)<li[^>]*>", "- ", body)
    text = html.unescape(re.sub(r"<[^>]+>", "", body))
    return re.sub(r"\n\s*\n+", "\n\n", text).strip()


def docx_to_text(path):
    """Paragraph and table text from word/document.xml, without third-party packages."""
    with zipfile.ZipFile(path) as z:
        info = z.getinfo("word/document.xml")
        if info.file_size > MAX_DOCX_XML:
            raise ValueError("document.xml too large")
        xml = z.read(info).decode("utf8", "replace")
    lines = []
    for para in re.findall(r"<w:p[ >].*?</w:p>", xml, re.S):
        runs = re.findall(r"<w:t(?: [^>]*)?>([^<]*)</w:t>|<w:(tab|br)/>", para)
        line = "".join(t if t else ("\t" if kind == "tab" else "\n") for t, kind in runs)
        lines.append(html.unescape(line))
    return "\n".join(lines).strip()


def pdf_to_text(path):
    out = subprocess.run(["pdftotext", "-layout", str(path), "-"], capture_output=True, text=True, timeout=60)
    return out.stdout.strip()


def extract(path):
    ext = path.suffix.lower().lstrip(".")
    if ext == "docx":
        return docx_to_text(path)
    if ext == "pdf":
        return pdf_to_text(path)
    if ext in TEXT_EXTS:
        return path.read_text(errors="replace")
    return None  # images and other binaries are reviewed as-is


def assignment_text(a):
    lines = [f"# {a['name']}", "", f"Points: {a.get('points_possible')}", f"Due: {a.get('due_at')}",
             f"Submission types: {', '.join(a.get('submission_types') or [])}", "", "## Instructions", "",
             html_to_text(a.get("description"))]
    if a.get("rubric"):
        lines += ["", "## Rubric", ""]
        for crit in a["rubric"]:
            lines.append(f"- {crit['description']} ({crit['points']} pts)")
            for r in crit.get("ratings", []):
                lines.append(f"    - {r['description']}: {r['points']} pts")
    return "\n".join(lines) + "\n"


def safe_name(name):
    return re.sub(r"[^\w.\- ]", "_", name).strip() or "file"


def cmd_list():
    for a in get_all(f"/courses/{COURSE}/assignments?per_page=100&include[]=submission_summary"):
        s = a.get("submission_summary") or {}
        print(f"{a['id']:>8}  {a['name'][:55]:55}  graded {s.get('graded', 0):>2}  "
              f"ungraded {s.get('ungraded', 0):>2}  not submitted {s.get('not_submitted', 0):>2}")


def cmd_show(aid):
    a, _ = api("GET", f"/courses/{COURSE}/assignments/{aid}?include[]=rubric")
    print(assignment_text(a))


def cmd_pull(aid):
    a, _ = api("GET", f"/courses/{COURSE}/assignments/{aid}?include[]=rubric")
    dest = OUT / str(aid)
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "assignment.md").write_text(assignment_text(a))
    index = []
    for s in get_all(f"/courses/{COURSE}/assignments/{aid}/submissions?per_page=100&include[]=user"):
        if s["workflow_state"] == "unsubmitted":
            continue
        name = s.get("user", {}).get("sortable_name") or str(s["user_id"])
        folder = dest / safe_name(name)
        folder.mkdir(exist_ok=True)
        files = []
        if s.get("body"):
            (folder / "online_text.txt").write_text(html_to_text(s["body"]))
            files.append("online_text.txt")
        for att in s.get("attachments") or []:
            path = folder / safe_name(att["filename"])
            req = urllib.request.Request(att["url"])
            with urllib.request.urlopen(req) as resp:
                path.write_bytes(resp.read())
            files.append(path.name)
            try:
                text = extract(path)
            except Exception as e:  # keep going; note the failure in the index
                text = f"[could not extract text: {e}]"
            if text is not None:
                (folder / f"{path.name}.txt").write_text(text)
                files.append(f"{path.name}.txt")
        index.append({"student": name, "user_id": s["user_id"], "state": s["workflow_state"],
                      "late": s.get("late"), "submitted_at": s.get("submitted_at"),
                      "score": s.get("score"), "files": files})
        print(f"pulled {name}: {', '.join(files) or 'no files'}")
    (dest / "index.json").write_text(json.dumps(index, indent=2))
    print(f"{len(index)} submissions in {dest}")


if __name__ == "__main__":
    args = sys.argv[1:]
    if args == ["list"]:
        cmd_list()
    elif len(args) == 2 and args[0] in ("show", "pull"):
        {"show": cmd_show, "pull": cmd_pull}[args[0]](args[1])
    else:
        sys.exit(__doc__)
