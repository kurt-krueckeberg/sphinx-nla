import xml.etree.ElementTree as ET


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
        else:
            out += render_inline(child)

        if child.tail:
            out += child.tail

    return out.strip()


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


def get_rows(elem):
    rows = []
    for row in elem.findall(".//row"):
        cells = row.findall("entry")
        if cells:
            rows.append(cells)
    return rows


def convert_simple_list_table(elem):
    rows = get_rows(elem)
    if not rows:
        return ""

    out = "::: {list-table}\n"
    out += ":header-rows: 1\n\n"

    for row in rows:
        out += f"* - {render_inline(row[0])}\n"
        for cell in row[1:]:
            out += f"  - {render_inline(cell)}\n"

    out += ":::\n\n"
    return out


def convert_flat_table(elem):
    rows = get_rows(elem)
    if not rows:
        return ""

    out = "```{eval-rst}\n"
    out += ".. flat-table::\n"
    out += "   :header-rows: 1\n\n"

    for row in rows:
        out += f"   * - {render_inline(row[0])}\n"

        for cell in row[1:]:
            attrs = []

            if "morerows" in cell.attrib:
                try:
                    attrs.append(f":rspan: {int(cell.attrib['morerows'])}")
                except ValueError:
                    pass

            if "namest" in cell.attrib and "nameend" in cell.attrib:
                attrs.append(":cspan: 1")

            # --- FIX: always emit a list item ---
            if attrs:
                out += f"     - {render_inline(cell)}\n"
                for attr in attrs:
                    out += f"       {attr}\n"
            else:
                out += f"     - {render_inline(cell)}\n"

    out += "```\n\n"
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

    for child in elem:
        out += convert_element(child, level)

    return out


def convert(doc):
    root = ET.parse(doc).getroot()
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
