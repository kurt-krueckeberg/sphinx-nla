#!/usr/bin/env python3

from pathlib import Path
import re

open_directive = re.compile(r'^(\s*)(`{3,}|~{3,})\{([^}]+)\}\s*(.*)$')
close_fence = re.compile(r'^(\s*)(`{3,}|~{3,})\s*$')

table_directives = {"list-table", "csv-table", "table"}

def has_doc_text(args):
    parts = args.replace(".", " ").split()
    return "doc-text" in parts

for path in Path(".").rglob("*.md"):
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    stack = []

    for lineno, line in enumerate(lines, start=1):
        m = open_directive.match(line)

        if m:
            indent, fence, directive, args = m.groups()
            directive = directive.strip()
            args = args.strip()

            inside_doc_text = any(
                d == "div" and has_doc_text(a)
                for d, a, f, start in stack
            )

            if directive in table_directives and inside_doc_text:
                div_start = next(
                    start for d, a, f, start in reversed(stack)
                    if d == "div" and has_doc_text(a)
                )
                print(
                    f"{path}:{lineno}: {directive} inside doc-text block "
                    f"starting at line {div_start}"
                )

            stack.append((directive, args, fence, lineno))
            continue

        m = close_fence.match(line)
        if m and stack:
            closing_fence = m.group(2)
            top_directive, top_args, opening_fence, start = stack[-1]

            # Close only if same fence character and at least as long.
            if (
                closing_fence[0] == opening_fence[0]
                and len(closing_fence) >= len(opening_fence)
            ):
                stack.pop()
