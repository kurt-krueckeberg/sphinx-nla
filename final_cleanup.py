import os
import re

def fix_content(content, current_file):
    if not content:
        return content

    # 1. FIX CROSS-REFERENCES
    # Converts Antora colons (689:page.adoc) to Sphinx paths (../689/page.md)
    # Also ensures standard .adoc links become .md
    def link_replacer(match):
        label = match.group(1)
        target = match.group(2)
        
        if ':' in target:
            # Handles multi-colon Antora paths like component:module:page
            parts = target.rsplit(':', 1)
            path_part = parts[0].replace(':', '/')
            page_part = parts[1].replace('.adoc', '.md')
            return f"[{label}](../{path_part}/{page_part})"
        
        # Simple local links
        new_target = target.replace('.adoc', '.md')
        return f"[{label}]({new_target})"

    content = re.sub(r'\[([^\]]+)\]\(([^)]+)\.adoc\)', link_replacer, content)
    # Catch cases where it was already .md but the path logic was wrong
    content = re.sub(r'\[([^\]]+)\]\(([^)]+\.md)\)', link_replacer, content)

    # 2. REMOVE INVALID CSS CLASSES (Pygments Lexer Errors)
    # Removes things like ' {.bordered}' or ' {.table}' after backticks
    content = re.sub(r'```\s*\{[\.\w-]+\}', '```', content)

    # 3. FIX EMPTY DIRECTIVES (Unknown Directive Errors)
    # Pandoc sometimes leaves '```{}' or empty directives
    content = re.sub(r'```\{\s*\}', '', content)
    
    return content

def generate_index_files(source_dir):
    """Generates an index.md with a toctree for every directory to fix 'Orphan' errors."""
    for root, dirs, files in os.walk(source_dir):
        # Don't overwrite existing indices
        if 'index.md' in files or 'index.rst' in files:
            continue
        
        md_files = [f for f in files if f.endswith('.md') and f != 'index.md']
        if not md_files:
            continue

        folder_name = os.path.basename(root).replace('-', ' ').title()
        index_path = os.path.join(root, 'index.md')
        
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(f"# {folder_name}\n\n")
            f.write("```{toctree}\n")
            f.write(":maxdepth: 1\n\n")
            for md in sorted(md_files):
                f.write(f"{md}\n")
            f.write("```\n")
        print(f"[INDEX CREATED] {index_path}")

def main():
    source_dir = './source'
    print("--- Starting Final Structural Bridge ---")
    
    # Pass 1: Content Fixes
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith(".md"):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    original = f.read()
                
                fixed = fix_content(original, path)
                
                if fixed != original:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(fixed)
                    print(f"[CLEANED] {path}")

    # Pass 2: Navigation Fixes (Orphans)
    generate_index_files(source_dir)
    print("--- Bridge Complete ---")

if __name__ == "__main__":
    main()
