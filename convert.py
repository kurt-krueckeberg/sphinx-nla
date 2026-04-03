import xml.etree.ElementTree as ET
import re
from decimal import Decimal, InvalidOperation
from math import gcd
from functools import reduce

def render_link(elem):
    ulink = elem.find("ulink")
    if ulink is not None:
        url = ulink.attrib.get("url", "")
        if url.endswith(".xml"):
            url = url[:-4] + ".md"
        label = "".join(ulink.itertext()).strip()

        return f"[{label or url}]({url})"
    return ""

def render_inline(elem):
    out = ""

    if elem.text:
        out += elem.text

    for child in elem:
        if child.tag == "emphasis":
            role = child.attrib.get("role", "")
            inner = render_inline(child)
            if role == "strong":
                out += f"**{inner}**"
            else:
                out += f"*{inner}*"

        elif child.tag == "xref":
            target = child.attrib.get("linkend", "")
            out += f"{{ref}}`{target}`"

        elif child.tag == "ulink":
            url = child.attrib.get("url", "")

            if url.endswith(".xml"):
                url = url[:-4] + ".md"

            label = render_inline(child) or url
            out += f"[{label}]({url})"

        elif child.tag == "link":
            out += render_link(child)

        else:
            out += render_inline(child)

        if child.tag != "link" and child.tail:
            out += child.tail

    return out.strip() if elem.tag in ("para", "simpara") else out


def render_cell_paragraphs(elem):
    paras = []

    for child in elem:
        if child.tag in ("simpara", "para"):
            text = render_inline(child)
            if text:
                paras.append(text)

    if paras:
        return paras

    text = render_inline(elem)
    return [text] if text else [""]


def convert_image(elem):
    img = elem.find(".//imagedata")
    if img is None:
        return ""

    src = img.attrib.get("fileref", "")
    title = elem.find(".//title")
    caption = render_inline(title) if title is not None else ""

    out = f"```{{figure}} {src}\n"
    if caption:
        out += caption + "\n"
    out += "```\n\n"
    return out


def convert_itemizedlist(elem):
    out = ""
    for item in elem.findall("listitem"):
        para = item.find(".//para")
        simpara = item.find(".//simpara")
        node = para if para is not None else simpara
        if node is not None:
            out += f"- {render_inline(node)}\n"
    return out + "\n"


def convert_orderedlist(elem):
    out = ""
    i = 1
    for item in elem.findall("listitem"):
        para = item.find(".//para")
        simpara = item.find(".//simpara")
        node = para if para is not None else simpara
        if node is not None:
            out += f"{i}. {render_inline(node)}\n"
            i += 1
    return out + "\n"


def cell_has_span(entry):
    return (
        "namest" in entry.attrib
        or "nameend" in entry.attrib
        or "morerows" in entry.attrib
    )


def table_has_spans(elem):
    for entry in elem.findall(".//entry"):
        if cell_has_span(entry):
            return True
    return False

def convert_admonition(elem):
    tag_to_name = {
        "note": "note",
        "tip": "tip",
        "important": "important",
        "warning": "warning",
        "caution": "caution",
    }

    admonition_type = tag_to_name.get(elem.tag)
    if not admonition_type:
        return ""

    out = f"```{{{admonition_type}}}\n"

    paras = []
    for child in elem:
        if child.tag in ("simpara", "para"):
            text = render_inline(child)
            if text:
                paras.append(text)
        else:
            rendered = convert_element(child)
            if rendered.strip():
                paras.append(rendered.strip())

    if paras:
        out += "\n\n".join(paras) + "\n"

    out += "```\n\n"
    return out

def get_rows(elem):
    rows = []
    for row in elem.findall(".//row"):
        cells = row.findall("entry")
        if cells:
            rows.append(cells)
    return rows

def parse_colwidth_value(colwidth):
    """
    Parse DocBook colwidth values like:
      17*
      72.25*
      42.5*
    Return Decimal or None.
    """
    if not colwidth:
        return None

    value = colwidth.strip()

    m = re.fullmatch(r'([0-9]+(?:\.[0-9]+)?)\*', value)
    if m:
        try:
            return Decimal(m.group(1))
        except InvalidOperation:
            return None

    m = re.fullmatch(r'([0-9]+(?:\.[0-9]+)?)', value)
    if m:
        try:
            return Decimal(m.group(1))
        except InvalidOperation:
            return None

    return None


def decimals_to_scaled_ints(values):
    """
    Convert Decimals to integers by scaling to the maximum number
    of decimal places present.
    Example: [42.5, 85, 297.5] -> [425, 850, 2975]
    """
    exponents = [abs(v.as_tuple().exponent) for v in values]
    scale = max(exponents) if exponents else 0
    factor = Decimal(10) ** scale
    return [int(v * factor) for v in values]


def reduce_ratio(ints):
    """
    Reduce a list of integers to lowest whole-number ratio.
    Example: [425, 850, 2975] -> [1, 2, 7]
    """
    g = reduce(gcd, ints)
    if g == 0:
        return ints
    return [n // g for n in ints]


def widths_from_colspecs(elem, prefer_ratio=True):
    """
    Read <colspec colwidth="..."> and return a MyST widths string.

    If prefer_ratio is True, return the lowest whole-number ratio:
      42.5*,85*,297.5* -> '1 2 7'

    Otherwise return integer percentages:
      17*,72.25*,335.75* -> '4 17 79'
    """
    tgroup = elem.find("tgroup")
    if tgroup is None:
        return None

    colspecs = tgroup.findall("colspec")
    if not colspecs:
        return None

    raw = []
    for colspec in colspecs:
        w = parse_colwidth_value(colspec.attrib.get("colwidth", ""))
        if w is None:
            return None
        raw.append(w)

    if not raw:
        return None

    if prefer_ratio:
        ints = decimals_to_scaled_ints(raw)
        ratio = reduce_ratio(ints)
        return " ".join(str(x) for x in ratio)

    total = sum(raw)
    if total == 0:
        return None

    exact = [(w * Decimal("100")) / total for w in raw]
    rounded = [int(x.to_integral_value(rounding="ROUND_HALF_UP")) for x in exact]

    diff = 100 - sum(rounded)
    if diff != 0:
        rounded[-1] += diff

    rounded = [max(1, x) for x in rounded]
    return " ".join(str(x) for x in rounded)

def emit_list_table_cell(paras, indent):
    out = f"{indent}- {paras[0]}\n"
    for para in paras[1:]:
        out += f"{indent}  \n"
        out += f"{indent}  {para}\n"
    return out


def emit_flat_table_cell(cell, indent):
    attrs = []

    if "morerows" in cell.attrib:
        try:
            attrs.append(f":rspan: {int(cell.attrib['morerows'])}")
        except ValueError:
            pass

    if "namest" in cell.attrib and "nameend" in cell.attrib:
        attrs.append(":cspan: 1")

    paras = render_cell_paragraphs(cell)
    out = ""

    if attrs:
        out += f"{indent}- {paras[0]}\n"
  
        for para in paras[1:]:
          out += f"{indent}  \n"
          for line in para.splitlines():
              out += f"{indent}  {line}\n"
  
        for attr in attrs:
            out += f"{indent}  {attr}\n"
    else:
        out += f"{indent}- {paras[0]}\n"
        for para in paras[1:]:
            out += f"{indent}  \n"
            for line in para.splitlines():
                out += f"{indent}  {line}\n"         
    
    return out

def parse_docbook_with_table_widths(doc):
    """
    Parse the DocBook file while preserving table-width processing instructions
    like <?dbhtml table-width="100%"?> by attaching the discovered width to
    the currently open table/informaltable element as a synthetic attribute
    named _table_width.
    """
    root = None
    table_stack = []

    for event, node in ET.iterparse(doc, events=("start", "end", "pi")):
        if event == "start":
            if root is None:
                root = node

            if node.tag in ("table", "informaltable"):
                table_stack.append(node)

        elif event == "pi":
            text = getattr(node, "text", "") or ""
            m = re.search(r'table-width="([^"]+)"', text)
            if m and table_stack:
                table_stack[-1].attrib["_table_width"] = m.group(1)

        elif event == "end":
            if node.tag in ("table", "informaltable"):
                if table_stack and table_stack[-1] is node:
                    table_stack.pop()

    return root

def table_width_from_pi(elem):
    """
    Return a table width such as '100%' if one was attached during parsing.
    """
    return elem.attrib.get("_table_width")

def header_rows_from_table(elem):
    """
    Return the number of header rows based on the DocBook table structure.

    For now, treat the presence of <thead> as one header row.
    If there is no <thead>, return 0.
    """
    thead = elem.find(".//thead")
    if thead is None:
        return 0

    rows = thead.findall("row")
    return len(rows) if rows else 1

def convert_simple_list_table(elem):
    rows = get_rows(elem)
    if not rows:
        return ""

    out = "::: {list-table}\n"

    table_width = table_width_from_pi(elem)
    if table_width:
        out += f":width: {table_width}\n"

    widths = widths_from_colspecs(elem, prefer_ratio=True)
    if widths:
        out += f":widths: {widths}\n"

    header_rows = header_rows_from_table(elem)
    if header_rows > 0:
        out += f":header-rows: {header_rows}\n"

    out += "\n"

    for row in rows:
        first_paras = render_cell_paragraphs(row[0])
        out += f"* - {first_paras[0]}\n"
        for para in first_paras[1:]:
            out += f"    \n"
            out += f"    {para}\n"

        for cell in row[1:]:
            paras = render_cell_paragraphs(cell)
            out += emit_list_table_cell(paras, "  ")

    out += ":::\n\n"
    return out

def convert_table(elem):
    title = elem.find("title")
    caption = render_inline(title) if title is not None else ""

    if table_has_spans(elem):
        out = convert_flat_table(elem)
    else:
        out = convert_simple_list_table(elem)

    if caption:
        return caption + "\n\n" + out
    return out

def convert_flat_table(elem):
    rows = get_rows(elem)
    if not rows:
        return ""

    out = "```{eval-rst}\n"
    out += ".. flat-table::\n"
    out += "   :header-rows: 1\n\n"

    for row in rows:
        first_paras = render_cell_paragraphs(row[0])
        out += f"   * - {first_paras[0]}\n"
        for para in first_paras[1:]:
            out += f"       \n"
            out += f"       {para}\n"

        for cell in row[1:]:
            out += emit_flat_table_cell(cell, "     ")

    out += "```\n\n"
    return out

def convert_element(elem, level=1):
    out = ""

    if "id" in elem.attrib:
        out += f"({elem.attrib['id']})=\n\n"

    if elem.tag in ("section", "sect1", "sect2"):
        title = elem.find("title")
        if title is not None:
            out += "#" * level + " " + render_inline(title) + "\n\n"

        for child in elem:
            if child.tag == "title":
                continue
            out += convert_element(child, level + 1)

        return out

    if elem.tag in ("para", "simpara"):
        return out + render_inline(elem) + "\n\n"

    if elem.tag in ("table", "informaltable"):
        return out + convert_table(elem)

    if elem.tag == "mediaobject":
        return out + convert_image(elem)

    if elem.tag == "itemizedlist":
        return out + convert_itemizedlist(elem)

    if elem.tag == "orderedlist":
        return out + convert_orderedlist(elem)

    if elem.tag in ("note", "tip", "important", "warning", "caution"):
        return out + convert_admonition(elem)

    if elem.tag == "literallayout":
        text = elem.text or ""
        role = elem.attrib.get("role", "").strip()

        out += "```{code-block} text\n"
        if role:
            out += f":class: {role}\n"
        out += "\n"
        out += text.rstrip("\n")
        out += "\n```\n\n" 
        return out

    for child in elem:
        out += convert_element(child, level)

    return out

def convert(doc):
    root = parse_docbook_with_table_widths(doc) 
    out = ""

    title = root.find("title")
    if title is None:
        info = root.find("info")
        if info is not None:
            title = info.find("title")

    if title is not None:
        out += "# " + render_inline(title) + "\n\n"

    for child in root:
        if child.tag in ("title", "info"):
            continue
        out += convert_element(child, level=2)

    return out


if __name__ == "__main__":
    import sys
    print(convert(sys.argv[1]))
