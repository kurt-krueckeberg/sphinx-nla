#!/usr/bin/env python3
"""
Batch-rewrite MyST/Markdown H1 headings while preserving the old H1 as an
archival Designatio Actorum description.

This script is intentionally batch-only:

  python3 rewrite_headers_archival_description.py --root ~/sphinx-nla --map titles.tsv
  python3 rewrite_headers_archival_description.py --root ~/sphinx-nla --map titles.tsv --in-place

The TSV map must have two tab-separated columns:

  relative/path/to/file.md<TAB>New shorter H1 title

Example:

  1237/doc1.md	1798 Krückeberg Petition
  1237/doc2.md	1798 Krückeberg Land Assignment Report

Only files listed in the TSV map are changed. Without --in-place, the script
only prints what it would do.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


H1_RE = re.compile(r"\A(---\n.*?\n---\n\s*)?#\s+(.+?)\s*$", re.DOTALL | re.MULTILINE)
ALREADY_DONE_RE = re.compile(
    r"##\s+Archival description\s+\*\*Designatio Actorum description:\*\*",
    re.IGNORECASE | re.DOTALL,
)


def read_title_map(map_path: Path) -> dict[str, str]:
    title_map: dict[str, str] = {}

    with map_path.open("r", encoding="utf-8") as f:
        for line_no, raw_line in enumerate(f, start=1):
            line = raw_line.rstrip("\n")

            if not line.strip() or line.lstrip().startswith("#"):
                continue

            if "\t" not in line:
                raise SystemExit(
                    f"ERROR: Bad line {line_no} in {map_path}.\n"
                    "Each non-comment line must contain: relative/path.md<TAB>New H1 title"
                )

            rel_path, new_title = line.split("\t", 1)
            rel_path = rel_path.strip()
            new_title = new_title.strip()

            if not rel_path:
                raise SystemExit(f"ERROR: Empty file path on line {line_no} in {map_path}")
            if not new_title:
                raise SystemExit(f"ERROR: Empty new H1 title on line {line_no} in {map_path}")
            if not rel_path.endswith(".md"):
                raise SystemExit(f"ERROR: File path does not end in .md on line {line_no}: {rel_path}")

            title_map[rel_path] = new_title

    if not title_map:
        raise SystemExit(f"ERROR: No usable entries found in {map_path}")

    return title_map


def rewrite_one_file(path: Path, new_title: str, in_place: bool) -> str:
    text = path.read_text(encoding="utf-8")

    if ALREADY_DONE_RE.search(text[:1500]):
        return "SKIP already rewritten"

    match = H1_RE.search(text)
    if not match:
        return "SKIP no H1 found"

    front_matter = match.group(1) or ""
    old_title = match.group(2).strip()

    replacement = (
        f"{front_matter}# {new_title}\n\n"
        "## Archival description\n\n"
        f"**Designatio Actorum description:** {old_title}\n"
    )

    new_text = text[: match.start()] + replacement + text[match.end() :]

    if in_place:
        path.write_text(new_text, encoding="utf-8")

    return f"UPDATE old H1: {old_title!r} -> new H1: {new_title!r}"


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Batch-rewrite Markdown H1 headers using a TSV map, preserving the old H1 "
            "as a Designatio Actorum description. Dry run by default."
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        "--root",
        required=True,
        help=(
            "Root folder containing the numeric case-file folders.\n"
            "Example: --root ~/sphinx-nla\n"
            "The map paths are interpreted relative to this folder."
        ),
    )

    parser.add_argument(
        "--map",
        required=True,
        dest="map_file",
        help=(
            "TSV file containing: relative/path.md<TAB>New shorter H1 title\n"
            "Example line: 1237/doc1.md<TAB>1798 Krückeberg Petition"
        ),
    )

    parser.add_argument(
        "--in-place",
        action="store_true",
        help="Actually modify files. Omit this for a dry run.",
    )

    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    map_path = Path(args.map_file).expanduser().resolve()

    if not root.is_dir():
        raise SystemExit(f"ERROR: --root is not a directory: {root}")
    if not map_path.is_file():
        raise SystemExit(f"ERROR: --map is not a file: {map_path}")

    title_map = read_title_map(map_path)

    mode = "IN-PLACE" if args.in_place else "DRY RUN"
    print(f"Mode: {mode}")
    print(f"Root: {root}")
    print(f"Map:  {map_path}")
    print()

    changed = 0
    skipped = 0

    for rel_path, new_title in sorted(title_map.items()):
        path = root / rel_path

        if not path.is_file():
            print(f"MISSING {rel_path}")
            skipped += 1
            continue

        result = rewrite_one_file(path, new_title, args.in_place)
        print(f"{rel_path}: {result}")

        if result.startswith("UPDATE"):
            changed += 1
        else:
            skipped += 1

    print()
    print(f"Updated: {changed}")
    print(f"Skipped/missing: {skipped}")

    if not args.in_place:
        print()
        print("Dry run only. Re-run with --in-place to modify files.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
