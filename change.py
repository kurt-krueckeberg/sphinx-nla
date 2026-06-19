#!/usr/bin/env python3

from pathlib import Path
import argparse
import re


DOC_TEXT_RE = re.compile(
    r"""^\s*(`{3,}|:{3,})\{div\}\s+doc-text\b.*$"""
)

OLD_LABEL_RE = re.compile(
    r"^\s*(?:#{1,6}\s*)?(?:\*\*)?(Transliteration\s+and\s+Translation|Transliteration|Translation)(?:\*\*)?\s*:?\s*(?:\{[^}]*\})?\s*$",
    re.IGNORECASE,
)

COMBINED_HEADER_RE = re.compile(
    r"^\s*(?:#{1,6}\s*)?(?:\*\*)?Transliteration\s+and\s+Translation(?:\*\*)?\s*:?\s*(?:\{[^}]*\})?\s*$",
    re.IGNORECASE,
)


def remove_old_labels_before_block(out_lines):
    """
    Remove old labels immediately before a doc-text block.

    Examples removed:

    ## Transliteration
    ### Translation
    Transliteration
    Translation
    **Transliteration**
    """
    while True:
        changed = False

        while out_lines and out_lines[-1].strip() == "":
            out_lines.pop()
            changed = True

        if out_lines and OLD_LABEL_RE.match(out_lines[-1]):
            out_lines.pop()
            changed = True
            continue

        if not changed:
            break

    return out_lines


def transform_text(text):
    lines = text.splitlines(keepends=True)
    out = []

    doc_text_count = 0

    for line in lines:
        # Remove old combined header wherever it appears.
        # This handles earlier failed runs that may have left it stranded.
        if COMBINED_HEADER_RE.match(line):
            continue

        if DOC_TEXT_RE.match(line):
            heading = (
                "## Transliteration\n"
                if doc_text_count % 2 == 0
                else "## Translation\n"
            )

            out = remove_old_labels_before_block(out)

            if out and out[-1].strip() != "":
                out.append("\n")

            out.append(heading)
            out.append("\n")
            out.append(line)

            doc_text_count += 1
        else:
            out.append(line)

    return "".join(out), doc_text_count


def process_file(path):
    original = path.read_text(encoding="utf-8")
    updated, count = transform_text(original)

    if updated != original:
        path.write_text(updated, encoding="utf-8")
        print(f"Updated: {path}")

    if count % 2 != 0:
        print(f"  WARNING: odd number of doc-text blocks found in {path}: {count}")

    return count


def main():
    parser = argparse.ArgumentParser(
        description="Normalize doc-text transliteration/translation headings."
    )
    parser.add_argument(
        "root",
        nargs="?",
        default=".",
        help="Project root directory. Defaults to current directory.",
    )

    args = parser.parse_args()
    root = Path(args.root).resolve()

    total_blocks = 0

    for path in sorted(root.rglob("*.md")):
        if any(part.startswith(".") for part in path.relative_to(root).parts):
            continue

        total_blocks += process_file(path)

    print()
    print(f"Total doc-text blocks found: {total_blocks}")


if __name__ == "__main__":
    main()
