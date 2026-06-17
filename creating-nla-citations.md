# Automating the Inclusion of Citations

## Citation Format and Philisophy

The philosophy of Evidence Explained is: cite the source at the level that
lets another researcher identify exactly what you used.

This format  describes the **archive container** and the **specific item inside that container**.
For Rentkammer case files the format would be:

###. For Rentkammer case file — specific Actenstück listed in the Designatio Actorum

```{div} doc-text
Niedersächsisches Landesarchiv, Abteilung Bückeburg [NLA BU], <case-file identifier>,
Actenstück <number>, "<German Designatio Actorum description>" [<English translation>],
in "<German case-file title>" [<English translation>], <case-file life span>;
Arcinsys Niedersachsen und Bremen, accessed <date>.
```

Example:

```{div} doc-text
Niedersächsisches Landesarchiv, Abteilung Bückeburg [NLA BU], L 1 Nr. 1234,
Actenstück 5, "Bericht des Amts Bückeburg wegen Ausweisung von Rottland"
[report of the Bückeburg office concerning the assignment of cleared land],
in "Acta betreffend den Colon Jobst Heinrich Krückeberg Nr. 10 zu Berenbusch"
[case file concerning Colon Jobst Heinrich Krückeberg no. 10 at Berenbusch],
1798–1800; Arcinsys Niedersachsen und Bremen, accessed 13 May 2026.
```

###. Rentkammer case file — additional document not listed in the Designatio Actorum

```{div} doc-text
Niedersächsisches Landesarchiv, Abteilung Bückeburg [NLA BU], <case-file identifier>,
document headed "<German document heading>" [<English translation>],
in "<German case-file title>" [<English translation>], <case-file life span>;
Arcinsys Niedersachsen und Bremen, accessed <date>.
```

Example:

```{div} doc-text
Niedersächsisches Landesarchiv, Abteilung Bückeburg [NLA BU], L 1 Nr. 1234,
document headed "Verkauf der Stätte Nr. 10 zu Berenbusch"
[sale of holding no. 10 at Berenbusch],
in "Acta betreffend den Colon Jobst Heinrich Krückeberg Nr. 10 zu Berenbusch"
[case file concerning Colon Jobst Heinrich Krückeberg no. 10 at Berenbusch],
1798–1800; Arcinsys Niedersachsen und Bremen, accessed 13 May 2026.
```

### Standalone archival document, not inside a case file

```{div} doc-text
Niedersächsisches Landesarchiv, Abteilung Bückeburg,
[<NLA BU archival identifier>](<Arcinsys URL>), "<German title or heading>"
[<English translation>].
```

Example:

```{div} doc-text
Niedersächsisches Landesarchiv, Abteilung Bückeburg,
[NLA BU L 2 L Nr. 27/28](https://www.arcinsys.niedersachsen.de/...),
"Cammeral-Kaufbrief für Jobst Heinrich Krückeberg Nr. 10 in Berenbusch"
[chamber purchase letter for Jobst Heinrich Krückeberg no. 10 in Berenbusch].
```

## Simple citation automation design

## Goal

Automatically insert bottom-of-page citations for documents listed in a case file’s **Designatio Actorum** table.

## Use one marker only

On each document page, add:

```md
<!-- citation: document=5 -->
```

Meaning:

```{div} doc-text
Use document 5 from the Designatio Actorum table.
```

## Inputs

### 1. Case metadata YAML

One YAML file per case file, for example:

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

### 2. Designatio Actorum page

This can contain either:

```{div} doc-text
raw HTML table
```

or:

```{div} doc-text
Markdown table
```

The table must include:

```{div} doc-text
document number | German description | English translation
```

### 3. Document pages

Each relevant page has one marker:

```md
<!-- citation: document=5 -->
```

## Script behavior

For each `.md` page:

1. find `<!-- citation: document=N -->`;
2. read the case metadata YAML;
3. open the Designatio Actorum page;
4. find document `N` in the table;
5. extract the German and English descriptions;
6. replace the marker with a generated citation section.

## Generated citation format

```md
## Citations

Niedersächsisches Landesarchiv, Abteilung Bückeburg [NLA BU], <case-file identifier>,
document <N>, "<German Designatio Actorum description>" [<English translation>],
in "<German case-file title>" [<English translation>], <case-file life span>;
Arcinsys Niedersachsen und Bremen, accessed <date>.
```

## Example output

```md
## Citations

Niedersächsisches Landesarchiv, Abteilung Bückeburg [NLA BU], L 1 Nr. 1234,
document 5, "Bericht des Amts Bückeburg wegen Ausweisung von Rottland"
[report of the Bückeburg office concerning the assignment of cleared land],
in "Acta betreffend den Colon Jobst Heinrich Krückeberg Nr. 10 zu Berenbusch"
[case file concerning Colon Jobst Heinrich Krückeberg no. 10 at Berenbusch],
1798–1800; Arcinsys Niedersachsen und Bremen, accessed 13 May 2026.
```

## Scope for first version

Handle only:

```{div} doc-text
document page → numbered Designatio Actorum row → generated citation
```

Do **not** handle standalone documents or unlisted documents automatically in the first version. Handle those manually.

