import os
import re
from bs4 import BeautifulSoup

def html_to_myst_list_table(html_content):
    """
    Parses raw HTML <table> tags and converts them into MyST blocks. 
    Uses linuxdoc.rstFlatTable via {eval-rst} for tables with spans.
    """
    try:
        # Use 'html.parser' to extract the table structure
        soup = BeautifulSoup(html_content, 'html.parser')
        table_node = soup.find('table')
        if not table_node:
            return html_content
            
        rows = table_node.find_all('tr')
        if not rows:
            return ""

        # Detect merged cells (spans) - critical for complex archival data
        has_merging = table_node.find(['td', 'th'], attrs={"colspan": True}) or \
                      table_node.find(['td', 'th'], attrs={"rowspan": True})
        
        # Extract column widths if present
        widths = []
        col_tags = table_node.find_all('col')
        for col in col_tags:
            style = col.get('style', '')
            width_match = re.search(r'width:\s*(\d+)%', style)
            if width_match:
                widths.append(width_match.group(1))
            elif col.get('width'):
                widths.append(col.get('width').replace('%', ''))

        myst = ""
        
        if has_merging:
            # Bridge to RST for complex tables using linuxdoc extension
            myst += "```{eval-rst}\n.. flat-table::\n"
            if widths:
                myst += f"   :widths: {' '.join(widths)}\n"
            myst += "   :header-rows: 1\n\n"  # MANDATORY BLANK LINE
            indent = "   " # Strict 3-space indentation for RST blocks
        else:
            # Standard MyST list-table for simple tables
            myst += "```{list-table}\n"
            if widths:
                myst += f":widths: {' '.join(widths)}\n"
            myst += ":header-rows: 1\n\n"
            indent = ""

        for row in rows:
            cols = row.find_all(['th', 'td'], recursive=False)
            if not cols:
                continue
            
            def clean_cell(cell):
                # Flattens internal HTML into plain text
                return cell.get_text(" ", strip=True).replace('\n', ' ').replace('\r', '')

            # Process the first cell of the row
            first_cell = cols[0]
            prefix = ""
            if has_merging:
                cs = first_cell.get('colspan')
                rs = first_cell.get('rowspan')
                # linuxdoc uses 0-based span indexing (extra cells to span)
                if cs and int(cs) > 1: prefix += f":cspan:`{int(cs)-1}` "
                if rs and int(rs) > 1: prefix += f":rspan:`{int(rs)-1}` "

            myst += f"{indent}* - {prefix}{clean_cell(first_cell)}\n"
            
            # Process remaining cells
            for col in cols[1:]:
                prefix = ""
                if has_merging:
                    cs = col.get('colspan')
                    rs = col.get('rowspan')
                    if cs and int(cs) > 1: prefix += f":cspan:`{int(cs)-1}` "
                    if rs and int(rs) > 1: prefix += f":rspan:`{int(rs)-1}` "
                myst += f"{indent}  - {prefix}{clean_cell(col)}\n"
        
        myst += "```\n"
        return myst
    except Exception as e:
        return f"\n\n> [!CAUTION] Table conversion failed: {e}\n\n{html_content}\n"

def cleanup_myst_syntax(content):
    """Fixes common MyST/Sphinx formatting issues."""
    # 1. Fix Admonitions (::: {.note} -> ```{note})
    content = re.sub(r'::: \{\.(note|important|warning|tip|caution)\}', r'```{\1}', content)
    
    # 2. Fix closing markers for blocks
    content = re.sub(r'^:::$', r'```', content, flags=re.MULTILINE)
    
    # 3. Handle formal paragraphs
    content = re.sub(r'::: \{\.formalpara-title\}\s*\n(.*?)\n:::', r'**\1**', content, flags=re.DOTALL)
    
    # 4. Clean up lingering Pandoc div containers
    content = re.sub(r':::\s*\{\.[\w-]+\}', '', content)
    
    return content

def process_md_file(md_path):
    """Searches for HTML tables and replaces them with MyST syntax."""
    try:
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Robust regex to catch <table> tags even with styles or classes
        table_pattern = re.compile(r'<table[^>]*>.*?</table>', re.DOTALL)
        
        if table_pattern.search(content):
            print(f"Converting tables in: {md_path}")
            content = table_pattern.sub(lambda m: html_to_myst_list_table(m.group(0)), content)
            content = cleanup_myst_syntax(content)

            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(content)
        else:
            # Optional: print files that were skipped
            # print(f"No HTML tables found in: {md_path}")
            pass
            
    except Exception as e:
        print(f"Error processing {md_path}: {e}")

def main():
    # Set this to your source directory containing the .md files
    base_dir = './source' 
    
    if not os.path.exists(base_dir):
        print(f"Directory {base_dir} not found. Please check your path.")
        return

    print("--- Starting HTML to MyST Table Migration ---")
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".md"):
                process_md_file(os.path.join(root, file))
    print("--- Migration Complete ---")

if __name__ == "__main__":
    main()
