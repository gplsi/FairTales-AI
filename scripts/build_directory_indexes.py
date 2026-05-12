#!/usr/bin/env python3
"""Generate static directory index pages for GitHub Pages."""

from __future__ import annotations

import html
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = ROOT / "runs-FairTales AI"
SKIP_FILES = {".DS_Store", "index.html"}


STYLE = """<style>
body{margin:0;background:#f7f5f0;color:#202124;font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;line-height:1.5}
main{max-width:1120px;margin:0 auto;padding:32px 20px 56px}
h1{margin:0 0 8px;font-size:clamp(1.6rem,4vw,2.6rem);line-height:1.08;overflow-wrap:anywhere}
p{margin:0 0 20px;color:#62656a}
a{color:#0f766e;text-decoration-thickness:.08em;text-underline-offset:.18em}
.top{display:flex;gap:16px;justify-content:space-between;align-items:flex-start;margin-bottom:24px}
.home{flex:0 0 auto;display:inline-flex;align-items:center;min-height:40px;padding:0 14px;border:1px solid #d8d2c8;border-radius:6px;background:#fff;color:#202124;text-decoration:none;font-weight:650}
.panel{border:1px solid #d8d2c8;border-radius:8px;background:#fff;overflow:hidden}
.row{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:16px;align-items:center;padding:12px 16px;border-top:1px solid #d8d2c8}
.row:first-child{border-top:0}
.name{min-width:0;overflow-wrap:anywhere;font-weight:650}
.meta{color:#62656a;white-space:nowrap;font-size:.92rem}
.badge{display:inline-flex;align-items:center;min-height:24px;border-radius:999px;padding:0 9px;background:#d8f3ee;color:#0b4f4a;font-size:.78rem;font-weight:700;text-transform:uppercase}
@media(max-width:680px){.top{display:grid}.home{width:max-content}.row{grid-template-columns:1fr;gap:6px}}
</style>"""


def sort_key(path: Path) -> tuple[int, str]:
    return (0 if path.is_dir() else 1, path.name.lower())


def file_size(bytes_count: int) -> str:
    if bytes_count < 1024:
        return f"{bytes_count} B"
    value = bytes_count / 1024
    for unit in ("KB", "MB", "GB"):
        if value < 1024 or unit == "GB":
            return f"{value:.0f} {unit}" if value >= 10 else f"{value:.1f} {unit}"
        value /= 1024
    return f"{bytes_count} B"


def href_for(path: Path, from_dir: Path) -> str:
    return html.escape(path.relative_to(from_dir).as_posix(), quote=True)


def relative_label(path: Path) -> str:
    return html.escape(path.relative_to(DATA_ROOT).as_posix() or DATA_ROOT.name)


def render_row(child: Path, from_dir: Path) -> str:
    label = html.escape(child.name)
    if child.is_dir():
        count = len([item for item in child.iterdir() if item.name not in SKIP_FILES])
        href = href_for(child, from_dir) + "/"
        return f'<div class="row"><a class="name" href="{href}">{label}</a><div class="meta"><span class="badge">Folder</span> {count} items</div></div>'

    href = href_for(child, from_dir)
    size = file_size(child.stat().st_size)
    return f'<div class="row"><a class="name" href="{href}">{label}</a><div class="meta"><span class="badge">File</span> {size}</div></div>'


def render_index(directory: Path) -> str:
    depth = len(directory.relative_to(ROOT).parts)
    home_href = "../" * depth + "index.html"
    parent_href = "../" if directory != DATA_ROOT else home_href
    rows = [
        render_row(child, directory)
        for child in sorted(directory.iterdir(), key=sort_key)
        if child.name not in SKIP_FILES
    ]
    if directory != DATA_ROOT:
        rows.insert(0, '<div class="row"><a class="name" href="../">..</a><div class="meta">Parent folder</div></div>')
    content = "\n".join(rows) if rows else '<div class="row"><span class="name">No files</span><div class="meta"></div></div>'

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{relative_label(directory)} - FairTales AI</title>
{STYLE}
</head>
<body>
<main>
<div class="top">
<div>
<h1>{relative_label(directory)}</h1>
<p>Static file listing for the FairTales AI dataset.</p>
</div>
<a class="home" href="{html.escape(home_href, quote=True)}">Back to overview</a>
</div>
<p><a href="{html.escape(parent_href, quote=True)}">Parent</a></p>
<section class="panel">
{content}
</section>
</main>
</body>
</html>
"""


def main() -> None:
    if not DATA_ROOT.exists():
        raise SystemExit(f"Missing data directory: {DATA_ROOT}")
    for directory in [DATA_ROOT, *[path for path in DATA_ROOT.rglob("*") if path.is_dir()]]:
        (directory / "index.html").write_text(render_index(directory), encoding="utf-8")


if __name__ == "__main__":
    main()
