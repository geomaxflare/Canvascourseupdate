#!/usr/bin/env python3
"""Build unpublished Canvas modules from a folder of Markdown pages.

Usage:
  python3 build_modules.py <course_id> <content_dir>

<content_dir> holds one folder per module, in order (01-..., 02-...). Each folder has:
  module.md     "# Module title", then "## Introduction" paragraphs and "## Objectives" bullets
  NN-slug.md    one teaching page each: "# Page title", then the body

Each module gets an overview page in the LCCC DesignPLUS template plus its teaching pages.
Modules, pages, and module items are all left unpublished. Re-running updates pages in place
(matched by title) instead of creating duplicates.
"""
import html
import re
import sys
import urllib.parse
from pathlib import Path

from canvas_pages import api, next_link

CSS = '<link rel="stylesheet" href="https://instructure-uploads.s3.amazonaws.com/account_38270000000000001/attachments/10338886/dp_app.css">'
JS = '<script src="https://instructure-uploads.s3.amazonaws.com/account_38270000000000001/attachments/10338885/dp_app.js"></script>'
PRE = '<pre style="background-color: #f5f5f5; border: 1px solid #ccc; padding: 10px; overflow-x: auto; font-size: 0.9em;"><code>{}</code></pre>'
TH = 'style="border: 1px solid #999; padding: 4px 8px; background-color: #f2f2f2; text-align: left;"'
TD = 'style="border: 1px solid #999; padding: 4px 8px;"'
H3 = 'style="background-color: #0055a4; color: #ffffff;"'
ICON = '<span class="dp-icon-content" style="display: none;">&nbsp;</span>'


def inline(text):
    text = html.escape(text, quote=False)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", text)
    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2" target="_blank">\1</a>', text)


def table(rows):
    cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
    head, body = cells[0], cells[2:]  # cells[1] is the --- separator
    out = ['<table style="border-collapse: collapse; margin: 1em 0;">', "<thead><tr>"]
    out += [f'<th scope="col" {TH}>{inline(c)}</th>' for c in head]
    out.append("</tr></thead><tbody>")
    for r in body:
        out.append("<tr>" + "".join(f"<td {TD}>{inline(c)}</td>" for c in r) + "</tr>")
    out.append("</tbody></table>")
    return "\n".join(out)


def md_to_html(md):
    """The Markdown subset the course pages use: ### headings, paragraphs, lists, code, tables."""
    lines, out, i = md.splitlines(), [], 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            code, i = [], i + 1
            while not lines[i].startswith("```"):
                code.append(lines[i])
                i += 1
            out.append(PRE.format(html.escape("\n".join(code), quote=False)))
            i += 1
        elif line.startswith("### "):
            out.append(f"<h3>{inline(line[4:])}</h3>")
            i += 1
        elif line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append(lines[i])
                i += 1
            out.append(table(rows))
        elif re.match(r"(- |\d+\. )", line):
            tag = "ul" if line.startswith("- ") else "ol"
            items = []
            while i < len(lines) and re.match(r"(- |\d+\. )", lines[i]):
                items.append(re.sub(r"^(- |\d+\. )", "", lines[i]))
                i += 1
            out.append(f"<{tag}>" + "".join(f"<li>{inline(t)}</li>" for t in items) + f"</{tag}>")
        elif line.strip():
            para = []
            while i < len(lines) and lines[i].strip() and not re.match(r"(```|### |\||- |\d+\. )", lines[i]):
                para.append(lines[i])
                i += 1
            out.append(f"<p>{inline(' '.join(para))}</p>")
        else:
            i += 1
    return "\n".join(out)


def split_title(md):
    first, _, rest = md.partition("\n")
    assert first.startswith("# "), "page must start with '# Title'"
    return first[2:].strip(), rest


def sections(md):
    return {m.group(1): m.group(2).strip() for m in re.finditer(r"^## (.+?)\n(.*?)(?=^## |\Z)", md, re.M | re.S)}


def overview_html(module_title, intro, objectives, activities):
    topic = module_title.split(": ", 1)[-1]
    number = module_title.split(":")[0]
    return f'''{CSS}<div id="dp-wrapper" class="dp-wrapper dp-flat-sections variation-2 cp-bg-dp-primary" style="background-color: #ffffff; color: #000000;" data-header-class="dp-header dp-flat-sections variation-2" data-nav-class="container-fluid dp-link-grid dp-flat-sections variation-2 dp-fs-2" data-img-url="https://designtools.ciditools.com/css/images/banner_desert_sky.png"><header class="dp-header dp-flat-sections variation-2 cp-bg-dp-primary" style="background-color: #0055a4; color: #ffffff;">
<h2 class="dp-heading cp-bg-dp-primary" style="background-color: #0055a4; color: #ffffff;"><span class="dp-header-pre" style="background-color: #ffc600; color: #000000;">{html.escape(topic)}&nbsp;</span>&nbsp;{html.escape(number)} Overview</h2>
</header>
<div class="dp-content-block">
{md_to_html(intro)}
<h3 class="dp-has-icon" {H3}><i class="dp-icon fas fa-atlas cp-out-info cp-bg-dp-secondary" aria-hidden="true">{ICON}</i> Objectives</h3>
<p>By the end of this module, you will be able to:</p>
{md_to_html(objectives)}
</div>
<div class="dp-content-block cp-bg-dp-white" style="color: #000000; background-color: #f5faff;">
<h3 class="dp-has-icon" {H3}><i class="dp-icon fas fa-laptop-code cp-bg-dp-secondary" aria-hidden="true">{ICON}</i> Activities and Assignments</h3>
<p>In this module, you will work through the following, in order:</p>
{activities}
</div>
</div>{JS}'''


def get_all(path):
    items, url = [], path
    while url:
        batch, link = api("GET", url)
        items.extend(batch)
        url = next_link(link)
    return items


def upsert_page(course, title, body):
    found = [p for p in get_all(f"/courses/{course}/pages?per_page=100&search_term={urllib.parse.quote(title)}")
             if p["title"] == title]
    data = {"wiki_page[title]": title, "wiki_page[body]": body, "wiki_page[published]": "false"}
    if found:
        page, _ = api("PUT", f"/courses/{course}/pages/{found[0]['url']}", data)
    else:
        page, _ = api("POST", f"/courses/{course}/pages", data)
    return page


def ensure_item(course, module_id, page, position, existing):
    for item in existing:
        if item.get("page_url") == page["url"]:
            api("PUT", f"/courses/{course}/modules/{module_id}/items/{item['id']}", {"module_item[position]": position})
            return item
    item, _ = api("POST", f"/courses/{course}/modules/{module_id}/items",
                  {"module_item[type]": "Page", "module_item[page_url]": page["url"],
                   "module_item[position]": position})
    return item


def build(course, content_dir):
    modules = {m["name"]: m for m in get_all(f"/courses/{course}/modules?per_page=100")}
    for folder in sorted(p for p in Path(content_dir).iterdir() if p.is_dir()):
        title, rest = split_title((folder / "module.md").read_text())
        parts = sections(rest)
        module = modules.get(title) or api("POST", f"/courses/{course}/modules",
                                           {"module[name]": title, "module[published]": "false"})[0]
        existing = get_all(f"/courses/{course}/modules/{module['id']}/items?per_page=100")
        overview_title = f"{title.split(':')[0]} Overview: {title.split(': ', 1)[-1]}"
        overview = upsert_page(course, overview_title, overview_html(title, parts["Introduction"], parts["Objectives"], ""))
        ensure_item(course, module["id"], overview, 1, existing)
        links = []
        for n, page_file in enumerate(sorted(folder.glob("[0-9]*.md")), start=2):
            page_title, body = split_title(page_file.read_text())
            page = upsert_page(course, page_title, CSS + md_to_html(body) + JS)
            item = ensure_item(course, module["id"], page, n, existing)
            links.append(f'<li>Read <a href="{item["html_url"]}">{html.escape(page_title)}</a>.</li>')
        upsert_page(course, overview_title, overview_html(title, parts["Introduction"], parts["Objectives"],
                                                          "<ol>" + "".join(links) + "</ol>"))
        api("PUT", f"/courses/{course}/modules/{module['id']}", {"module[published]": "false"})
        print(f"{title}: overview + {len(links)} pages (unpublished)")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    build(sys.argv[1], sys.argv[2])
