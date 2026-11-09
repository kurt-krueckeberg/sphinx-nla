# Rentkammer Case Files: Presentation Guide

This guide covers the seven Rentkammer case files in `sphinx-nla` (1237, 1291, 139,
146, 147, 188, 689). The general documents (140, 2713, 2728, 2741) are not case
files and are not covered.

## What the case files do now

The content is strong. The presentation differs from file to file in five ways.

**Where a case file begins.** 1237, 1291 and 689 open on the Designatio Actorum
(`content.md`). 139, 146 and 188 open on an `index.md` with a narrative. 147 opens
on its cover. 1291, 147 and 188 have no narrative overview at all. The narrative
material that does exist is spread across several kinds of page:

- `intro.md` in 1237 and 689
- `timeline.md` in 1237 and 139
- `amt-decree.md` in 689
- two analyses of Document 1 in 146, placed ahead of the cover

**Order of pages.** In 139 the timeline comes before the cover. In 146 the
analyses come before the cover. In 689 the overview of the Amt decree comes before
Document 1.

**The Designatio Actorum.** 1237 and 139 use `list-table`. The others use
`flat-table`. The columns differ from file to file. The heading is spelled four
ways: "Designatio Actorum", "Designation Actorum" (1291, 689), "Contents List" and
"Table of Contents".

**Document pages.** The introductory section has seven names: Overview, Summary,
Narrative Overview, Narrative Summary, Document Summary, Explanation and Comments.
Almost every page in 1291 and 188 has none. Image sections have four names: Image,
Images, Digital Image and Digital Images. Several pages also have empty wrapper
headings such as "Transliteration and Translation" (sometimes misspelled
"Transliateration"). A few pages in 689 put transliteration and translation side
by side in a `list-table`. Everywhere else they come one after the other in
`doc-text` boxes. Titles carry a date in 139 and 1237, carry none in 1291, and in
the 1850 pages of 146 put the date first.

**Documents with several parts.** A docket page, the petition and a marginal
resolution are all handled with H2 headings. As a result, "Transliteration" and
"Translation" appear several times at the same level, and the page's right-hand
outline becomes a column of identical entries.

Glossaries are also repeated page by page (1237, 139, 1291/doc22), although
`rentkammer/terms.md` already exists. Finally, apart from 140, none of the pages
carries an archival citation.

Your 139 document pages, such as `jh-krueckeberg-petition-to-sell.md`, come
closest to the pattern recommended below. 1291 and 188 are furthest from it.

## Recommended structure for a case file

Every case file should have the same sequence in `_toc.yml`:

1. **`index.md`**: the landing page and chapter entry (layout below)
2. **`cover.md`**: the case file cover
3. **`content.md`**: the Designatio Actorum
4. **Documents**, in Designatio order
5. **Later documents**, if any (as in 139 and 146), grouped under their own short
   overview page
6. **Supplementary studies**, if any (the doc1 analyses in 146, the
   numbering notes in 689), placed last and not ahead of the cover

Give every document a `title:` in `_toc.yml` in the same form: *Type of document,
who* (*date*). For example: *Petition of the widow Krückeberg (8 Jul 1824)*.

### Landing page (`index.md`)

````md
# Site No. 10 in Berenbusch: Relief from Labour Services and Sale (1824–1849)

## Overview

Narrative overview in plain prose: who the people are, what they asked for,
what the Rentkammer decided, and what the file tells us about the family.
Link to documents as you mention them, e.g. the [widow's petition](doc1-1.md).

```{list-table}
:widths: 25 75

* - Archive reference
  - [NLA BU, L 101a, A Nr. 139](arcinsys-link)
* - Date span
  - 1824–1849
* - Holding
  - Stätte No. 10, Berenbusch
* - Principal persons
  - Widow Krückeberg; Johann Heinrich Krückeberg (1806–1879); Wilhelm Bornemann
* - Outcome
  - Labour services remitted (1824); sale approved before emigration (1849)
```

## Timeline

Optional. Use one only when the file covers more than one episode or its
documents are out of date order. Keep it to a compressed table, with each row
linking to its document.

## Citation

Niedersächsisches Landesarchiv, Abteilung Bückeburg, NLA BU, L 101a, A Nr. 139,
"German case-file title" [English title], 1824–1849.
````

Fold the material now in `intro.md`, `timeline.md` and the narrative part of
`content.md` into this page, so that each case file has one place to start.

### Designatio Actorum (`content.md`)

````md
# Designatio Actorum

One or two sentences on what the Designatio is, linking to
[Case Files Explained](../rentkammer/case-file-docs-explained.md).

```{figure} images/01.png
:class: image-override
```

```{flat-table}
:class: no-zebra-rowspan-table
:header-rows: 1

* - No.
  - Document
  - Subject
  - Place
  - Date
* - 1\.
  - [Petition of …](doc1.md)

    [Vorstellung des …](doc1.md)
  - English subject

    German Betreff
  - Bburg
  - 29 May 1798
```
````

Always use `flat-table`, because the Betreff column often needs `rspan`. Always use
the same five columns, with English first and German below it, as you already do.
Put Jahr, Monat and Tag together in one Date column in the form *29 May 1798*. Use
that form for dates everywhere in the book.

### Document page

````md
# Report of the Bückeburg Office (26 Jul 1824)

:::{admonition} Document details
:class: dropdown

Designatio item
: 1 (second document)

Registry number
: N.C. 2816

From / to
: Amt Bückeburg → Rentkammer
:::

## Overview

What the document is, why it was written, what it says, and what it means for
the case. This is where your current commentary goes.

:::{admonition} What were Burgrest-Handtage?
Context-specific explanations stay as admonitions here.
:::

## Images

```{figure} images/02.png
:class: image-override
```

## Text

::::{tab-set}
:::{tab-item} Translation
```{div} doc-text
English translation
```
:::
:::{tab-item} Transliteration
```{div} doc-text
German transliteration
```
:::
::::

## Notes

Translation notes, docket marks and numbering observations (optional).
````

Use only these headings, in this order: **Overview, Images, Text, Notes**. Leave
out a section when it has nothing in it, rather than renaming it.

The tabs come from `sphinx_design`, which `_config.yml` already loads but no page
uses yet. Putting Translation in the first tab means the reader lands on the
English. Anyone checking your reading of the German is one click away from the
transliteration. The page also stays half as long, which matters for the many
two- and three-page documents. The side-by-side tables in 689 should be changed to
this same form.

### Documents with several parts

Write the overview once, at the top. Then give each physical part its own H2
heading, with Images and Text as H3 headings inside it:

````md
## Overview

## Part 1: Docket page
### Images
### Text

## Part 2: Petition
### Images
### Text

## Part 3: Marginal resolution of the Rentkammer
### Images
### Text
````

The right-hand outline then reads "Docket page / Petition / Marginal resolution"
instead of six identical "Transliteration / Translation" entries.

### Glossary

Move the per-page glossaries into `rentkammer/terms.md` and make it a MyST
`{glossary}`. Pages can then link a term with `` {term}`Brinksitzer` ``, and each
definition is kept in one place. Admonitions remain the right tool for an
explanation that only matters on one page.

## Order of work

If you adopt this pattern, change 139 first, because its pages need only renamed
headings and the tabs. Then use it as the model for the others. 1291 and 188 will
take the most work, because their overviews have to be written rather than moved.
````
