# Automating the Inclusion of Citations

## Citation Format and Philisophy

The philosophy of Evidence Explained is: cite the source at the level that
lets another researcher identify exactly what you used.

This format  describes the **archive container** and the **specific item inside that container**.
For Rentkammer case files the format would be:

1. For Rentkammer case file — specific Actenstück listed in the Designatio Actorum

```text
Niedersächsisches Landesarchiv, Abteilung Bückeburg [NLA BU], <case-file identifier>,
Actenstück <number>, "<German Designatio Actorum description>" [<English translation>],
in "<German case-file title>" [<English translation>], <case-file life span>;
Arcinsys Niedersachsen und Bremen, accessed <date>.
```

Example:

```text
Niedersächsisches Landesarchiv, Abteilung Bückeburg [NLA BU], L 1 Nr. 1234,
Actenstück 5, "Bericht des Amts Bückeburg wegen Ausweisung von Rottland"
[report of the Bückeburg office concerning the assignment of cleared land],
in "Acta betreffend den Colon Jobst Heinrich Krückeberg Nr. 10 zu Berenbusch"
[case file concerning Colon Jobst Heinrich Krückeberg no. 10 at Berenbusch],
1798–1800; Arcinsys Niedersachsen und Bremen, accessed 13 May 2026.
```

2. Rentkammer case file — additional document not listed in the Designatio Actorum

```text
Niedersächsisches Landesarchiv, Abteilung Bückeburg [NLA BU], <case-file identifier>,
document headed "<German document heading>" [<English translation>],
in "<German case-file title>" [<English translation>], <case-file life span>;
Arcinsys Niedersachsen und Bremen, accessed <date>.
```

Example:

```text
Niedersächsisches Landesarchiv, Abteilung Bückeburg [NLA BU], L 1 Nr. 1234,
document headed "Verkauf der Stätte Nr. 10 zu Berenbusch"
[sale of farmstead no. 10 at Berenbusch],
in "Acta betreffend den Colon Jobst Heinrich Krückeberg Nr. 10 zu Berenbusch"
[case file concerning Colon Jobst Heinrich Krückeberg no. 10 at Berenbusch],
1798–1800; Arcinsys Niedersachsen und Bremen, accessed 13 May 2026.
```

3. Standalone archival document, not inside a case file

```text
Niedersächsisches Landesarchiv, Abteilung Bückeburg [NLA BU], <identifier>,
"<German document title or heading>" [<English translation>], <date or life span>;
Arcinsys Niedersachsen und Bremen, accessed <date>.
```

Example:

```text
Niedersächsisches Landesarchiv, Abteilung Bückeburg [NLA BU], L 1 Nr. 5678,
"Cammeral-Kaufbrief für Jobst Heinrich Krückeberg Nr. 10 in Berenbusch"
[chamber purchase letter for Jobst Heinrich Krückeberg no. 10 in Berenbusch],
10 March 1799; Arcinsys Niedersachsen und Bremen, accessed 13 May 2026.
```

## Implementation

### Goal

Automatically replace page markers like:

```md
<!-- citation: document=5 -->
```

with full archival citation sections.

### Inputs

1. **Case metadata YAML**, one per case file:

```yaml
case_file:
  identifier: "L 1 Nr. 1234"
  german_title: "Acta betreffend ..."
  english_title: "case file concerning ..."
  life_span: "1798–1800"
  archive: "Niedersächsisches Landesarchiv, Abteilung Bückeburg"
  archive_short: "NLA BU"
  catalog: "Arcinsys Niedersachsen und Bremen"
  accessed: "13 May 2026"
  designatio_page: "designatio-actorum.md"
```

2. **Designatio Actorum page**

Either raw HTML table or Markdown table.

Must contain, somehow:

```text
document number | German description | English translation
```

3. **Document pages**

Each page has a marker:

```md
<!-- citation: document=5 -->
```

### Script behavior

For each `.md` page:

1. find citation marker;
2. identify the relevant case-file YAML;
3. read the Designatio Actorum table;
4. find the matching document row;
5. generate citation;
6. insert/replace:

```md
## Citations

Niedersächsisches Landesarchiv, Abteilung Bückeburg [NLA BU], L 1 Nr. 1234,
document 5, "German description" [English translation], in "German case-file title"
[English case-file title], 1798–1800; Arcinsys Niedersachsen und Bremen, accessed
13 May 2026.
```

### Citation marker options

Listed document:

```md
<!-- citation: document=5 -->
```

Unlisted document:

```md
<!-- citation: heading="Verkauf der Stätte Nr. 10 zu Berenbusch" translation="sale of farmstead no. 10 at Berenbusch" -->
```

Standalone document:

```md
<!-- citation: standalone -->
```

### Output

Same `.md` files, now with generated `## Citations` sections.

### Best implementation

Python script using:

```text
PyYAML + BeautifulSoup + markdown-table parser/simple regex
```

No BibTeX needed.

