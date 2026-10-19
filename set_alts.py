#!/usr/bin/env python3
"""Set image alt text on pulled Canvas pages and push them.

Usage: python3 set_alts.py alts.json
alts.json maps page slug -> {file_id: alt text}.
"""
import html
import json
import re
import sys

import canvas_pages as c


def set_alts(body, alts):
    def repl(m):
        tag = m.group(0)
        fid = re.search(r"/files/(\d+)", tag)
        if not fid or fid.group(1) not in alts:
            return tag
        alt = html.escape(alts[fid.group(1)], quote=True)
        done.add(fid.group(1))
        if re.search(r'\balt="[^"]*"', tag):
            return re.sub(r'\balt="[^"]*"', f'alt="{alt}"', tag, count=1)
        return tag.replace("<img", f'<img alt="{alt}"', 1)

    done = set()
    body = re.sub(r"""<img\b(?:[^>"']|"[^"]*"|'[^']*')*>""", repl, body)
    missing = set(alts) - done
    if missing:
        raise SystemExit(f"image ids not found on page: {sorted(missing)}")
    return body


if __name__ == "__main__":
    plan = json.load(open(sys.argv[1]))
    for slug, alts in plan.items():
        live, _ = c.api("GET", f"/courses/{c.COURSE}/pages/{slug}")
        local = (c.PAGES / f"{slug}.html").read_text()
        if (live.get("body") or "") != local:
            raise SystemExit(f"{slug} changed in Canvas since pull; re-pull first")
        (c.PAGES / f"{slug}.html").write_text(set_alts(local, alts))
    c.push(list(plan))
