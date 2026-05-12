#!/usr/bin/env python3
"""Build a static file manifest for the GitHub Pages data browser."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = ROOT / "runs-FairTales AI"
OUTPUT = ROOT / "data-manifest.json"
SKIP_FILES = {".DS_Store", "index.html"}


def sort_key(path: Path) -> tuple[int, str]:
    return (0 if path.is_dir() else 1, path.name.lower())


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def build_directory(path: Path) -> dict[str, object]:
    directories = []
    files = []

    for child in sorted(path.iterdir(), key=sort_key):
        if child.name in SKIP_FILES:
            continue
        if child.is_dir():
            directories.append(
                {
                    "name": child.name,
                    "path": relative(child),
                    "children": build_directory(child),
                }
            )
        elif child.is_file():
            files.append(
                {
                    "name": child.name,
                    "path": relative(child),
                    "size": child.stat().st_size,
                }
            )

    return {"directories": directories, "files": files}


def main() -> None:
    if not DATA_ROOT.exists():
        raise SystemExit(f"Missing data directory: {DATA_ROOT}")

    manifest = {
        "root": DATA_ROOT.name,
        "generated_from": relative(DATA_ROOT),
        "tree": build_directory(DATA_ROOT),
    }
    OUTPUT.write_text(json.dumps(manifest, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")


if __name__ == "__main__":
    main()
