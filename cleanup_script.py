import os
import re

def clean_myst_files(source_dir):
    image_pattern = re.compile(r'!\[(.*?)\]\((?:\d+:|.*?:)(.*?\.(?:jpg|png|gif|svg|jpeg))\)')
    xref_pattern = re.compile(r'\[(.*?)\]\(xref:(.*?)\.adoc\)')

    malformed_colon_blocks = re.compile(r'^:::\s*\{.*?\}.*?^:::$', re.MULTILINE | re.DOTALL)
    empty_fenced_directives = re.compile(r'```{\s*}\s*```|```{\s*}\s*\n', re.MULTILINE)

    print("Starting cleanup in:", source_dir)

    for root, _, files in os.walk(source_dir):
        for file in files:
            if not file.endswith('.md'):
                continue

            file_path = os.path.join(root, file)

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content

            content = image_pattern.sub(r'![\1](images/\2)', content)
            content = xref_pattern.sub(r'[\1](\2.md)', content)
            content = malformed_colon_blocks.sub('', content)
            content = empty_fenced_directives.sub('', content)
            content = re.sub(r'[ \t]+$', '', content, flags=re.MULTILINE)

            if file == 'nav.md':
                content = transform_to_toctree(content, root, source_dir)

            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print("Fixed:", file_path)

def transform_to_toctree(content, current_dir, source_dir):
    lines = content.splitlines()

    new_lines = [
        "```{toctree}",
        ":maxdepth: 2",
        ":caption: Contents",
        ""
    ]

    found = False

    for line in lines:
        match = re.search(r'\[.*?\]\((.*?)\)', line)
        if not match:
            continue

        raw_path = match.group(1).strip()
        raw_path = raw_path.split('#')[0]

        if not raw_path:
            continue

        if raw_path.startswith('xref:'):
            raw_path = raw_path.replace('xref:', '')
            raw_path = raw_path.replace('.adoc', '.md')

        raw_path = raw_path.replace('\\', '/').strip()

        abs_path = os.path.normpath(os.path.join(current_dir, raw_path))

        try:
            rel_path = os.path.relpath(abs_path, source_dir)
        except ValueError:
            continue

        rel_path = re.sub(r'\.md$', '', rel_path)

        md_file = os.path.join(source_dir, rel_path + '.md')
        if not os.path.exists(md_file):
            continue

        rel_path = rel_path.replace('\\', '/')
        new_lines.append(f"    {rel_path}")
        found = True

    if found:
        new_lines.append("```")
        return "\n".join(new_lines)

    return content

if __name__ == "__main__":
    TARGET_DIR = "./source"

    if os.path.exists(TARGET_DIR):
        clean_myst_files(TARGET_DIR)
        print("\nCleanup complete. Run: make clean && make html")
    else:
        print(f"Error: Directory {TARGET_DIR} not found.")
