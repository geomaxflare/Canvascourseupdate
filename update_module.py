#!/usr/bin/env python3
"""Fill an existing Canvas module from a folder of Markdown, keeping it unpublished.

Usage:
  python3 update_module.py <course_id> <content_dir>

<content_dir> holds:
  module.md        "# Module N: Title", then Introduction, Objectives, and any other "## " sections
                   (shown on the overview before the activity list, e.g. TILT purpose and criteria)
  NN-slug.md       teaching pages, in order
  assignment*.md   optional: "# Assignment name", then its description
  module.json      canvas_module (existing module name), overview_title, assignment settings
                   ("assignment" for assignment.md, or an "assignments" list naming each file,
                   optionally only_visible_to_overrides), and trailing items to keep at the end

New pages and the assignment are created unpublished. Re-running updates them in place.
"""
import html
import json
import sys
import urllib.parse
from pathlib import Path

from build_modules import CSS, JS, api, get_all, md_to_html, overview_html, sections, split_title, upsert_page


def place(course, module_id, existing, position, **match_and_create):
    """Find the module item matching the given content, or create it, then set its position."""
    kind = match_and_create["type"]
    for item in existing:
        if item["type"] == kind and (
            (kind == "Page" and item.get("page_url") == match_and_create.get("page_url"))
            or (kind in ("Assignment", "File") and item.get("content_id") == match_and_create.get("content_id"))
            or (kind == "SubHeader" and item["title"] == match_and_create.get("title"))):
            api("PUT", f"/courses/{course}/modules/{module_id}/items/{item['id']}", {"module_item[position]": position})
            return item
    data = {f"module_item[{k}]": v for k, v in match_and_create.items()}
    data["module_item[position]"] = position
    item, _ = api("POST", f"/courses/{course}/modules/{module_id}/items", data)
    return item


def upsert_assignment(course, name, body, settings):
    query = urllib.parse.quote(name)
    found = [a for a in get_all(f"/courses/{course}/assignments?per_page=100&search_term={query}") if a["name"] == name]
    data = [("assignment[name]", name), ("assignment[description]", body),
            ("assignment[points_possible]", settings["points"]),
            ("assignment[assignment_group_id]", settings["group_id"]),
            ("assignment[published]", "false"),
            # visible only to students given an override (for example, an opt-out alternative)
            ("assignment[only_visible_to_overrides]", str(settings.get("only_visible_to_overrides", False)).lower())]
    data += [("assignment[submission_types][]", t) for t in settings["submission_types"]]
    if found:
        a, _ = api("PUT", f"/courses/{course}/assignments/{found[0]['id']}", data)
    else:
        a, _ = api("POST", f"/courses/{course}/assignments", data)
    return a


def update(course, content_dir):
    folder = Path(content_dir)
    cfg = json.loads((folder / "module.json").read_text())
    title, rest = split_title((folder / "module.md").read_text())
    parts = sections(rest)
    extras = [(k, v) for k, v in parts.items() if k not in ("Introduction", "Objectives")]
    module = [m for m in get_all(f"/courses/{course}/modules?per_page=100") if m["name"] == cfg["canvas_module"]][0]
    existing = get_all(f"/courses/{course}/modules/{module['id']}/items?per_page=100")

    overview = upsert_page(course, cfg["overview_title"],
                           overview_html(title, parts["Introduction"], parts["Objectives"], "", extras, extras_first=True))
    place(course, module["id"], existing, 1, type="Page", page_url=overview["url"])
    pos, links = 2, []
    for page_file in sorted(folder.glob("[0-9]*.md")):
        page_title, body = split_title(page_file.read_text())
        page = upsert_page(course, page_title, CSS + md_to_html(body) + JS)
        item = place(course, module["id"], existing, pos, type="Page", page_url=page["url"])
        links.append(f'<li>Read <a href="{item["html_url"]}">{html.escape(page_title)}</a>.</li>')
        pos += 1
    assignments = cfg.get("assignments") or ([dict(cfg["assignment"], file="assignment.md")]
                                             if (folder / "assignment.md").exists() else [])
    if assignments:
        place(course, module["id"], existing, pos, type="SubHeader", title="Assignment")
        pos += 1
    for settings in assignments:
        name, body = split_title((folder / settings["file"]).read_text())
        assignment = upsert_assignment(course, name, CSS + md_to_html(body) + JS, settings)
        item = place(course, module["id"], existing, pos, type="Assignment", content_id=assignment["id"])
        if settings.get("only_visible_to_overrides"):
            links.append(f'<li>Or, if you have chosen not to use AI and your instructor has assigned it to you, complete <a href="{item["html_url"]}">{html.escape(name)}</a>.</li>')
        else:
            links.append(f'<li>Complete <a href="{item["html_url"]}">{html.escape(name)}</a>.</li>')
        pos += 1
    for extra in cfg.get("trailing", []):
        if "subheader" in extra:
            place(course, module["id"], existing, pos, type="SubHeader", title=extra["subheader"])
        else:
            place(course, module["id"], existing, pos, type="File", content_id=extra["file_id"])
        pos += 1
    upsert_page(course, cfg["overview_title"],
                overview_html(title, parts["Introduction"], parts["Objectives"], "<ol>" + "".join(links) + "</ol>",
                              extras, extras_first=True))
    print(f"{cfg['canvas_module']}: overview + {len(links)} activities, {pos - 1} items (new content unpublished)")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    update(sys.argv[1], sys.argv[2])
