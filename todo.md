# todo

[JB 1](https://jupyterbook.org/v1/structure/configure.html)

## Create _toc.yml

Use the **Jupyter Book 2 `toc:` as the working basis**, but not because JB2
is the final website. Use it because it is the **most recent expression of
your intended structure**.

Suggested method:

```text
1. Treat the JB2 toc as the draft master outline.
2. Restore meaningful titles where you over-shortened them.
3. Ignore the repaint bug while designing titles.
4. Aim for titles that are clear, not ultra-short.
5. Then translate that outline into:
   - Antora nav.adoc
   - JB1 _toc.yml
   - JB2 myst.yml for PDF/export
```

A good title rule:

```text
Short enough to scan,
long enough to mean something.
```

Do **not** design around the JB2 repaint bug anymore. That led you to over-compress the text.

For your case-file material, I’d use a consistent pattern like:

```text
1798 Petition
1798 Land Report
1798 Chamber Response
1799 Resubmission
1800 Final Decision
```

rather than:

```text
Doc. 1
Doc. 2
Doc. 3
```

or overlong archival titles.

So yes: start from the JB2 `toc:`, but revise it as a **content outline**,
not as a workaround for JB2’s static navigation flaw.

For the 2nd-level navigation, use this guidance:
Yes.

Use this rule:

```text
H1 = full archival/page title
nav title = shorter, readable, still identifiable
```

Do **not** shorten so much that the title loses the person, place, year, or document type.

A good second-level nav title should usually include:

```text
year + key person/place + document type
```

Examples:

```text
H1:
Document 1: Jobst Heinrich Krückeberg Petition (29 May 1798)

Nav:
1798 Krückeberg Petition
```

```text
H1:
Document 2: Report Concerning Jobst Heinrich Krückeberg’s Requested Land Assignment

Nav:
1798 Krückeberg Land Report
```

```text
H1:
Document 3: Rentkammer Response Concerning the Krückeberg Petition

Nav:
1798 Rentkammer Response
```

```text
H1:
Document 4: Reminder Note Concerning the Krückeberg Land Request

Nav:
1799 Krückeberg Reminder
```

Working method:

```text
1. Extract all H1 headings.
2. Group repeated document types: Petition, Report, Response, Note, Survey, List, Map, Translation.
3. Create one standard nav-title pattern for each type.
4. Keep the H1s full and descriptive.
5. Use the shorter titles only in Antora nav, JB1 _toc.yml, and JB2 myst.yml.
```

Suggested patterns:

```text
YYYY Person Petition
YYYY Person Land Report
YYYY Rentkammer Response
YYYY Person Reminder
YYYY Place Survey
YYYY Household List
YYYY Property Register
YYYY Map/Sketch
YYYY Translation
```

For your site, I would favor titles like:

```text
1798 Krückeberg Petition
1798 Krückeberg Land Report
1798 Rentkammer Response
1799 Krückeberg Resubmission
1800 Final Decision
1737 Householder Survey
1743 Property Questioning
1745 Evesen–Berenbusch Survey
1747 Kolon List
```

That keeps the navigation compact without making it cryptic.

