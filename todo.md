# todo

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

