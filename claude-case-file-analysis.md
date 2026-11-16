# Claude Analysis (done on 11/16/2026)

Starting with the Context doc and the repository: reading the folder list, then comparing each
folder's `_toc.yml` entries and markdown content.

**Result:** the `_toc.yml` is consistent only at the top level, and folder 139 is the best
model. I changed nothing in the repository.

## Navigation consistency

All seven folders start with `index` → `cover` → `content` (188 has no `content` because it has no Designatio Actorum). Below that they diverge:

- **Chapter titles:** each uses a different form. 1237 and 188 carry no dates, 146 puts the dates after a comma, 147 is two lines long, and 139 has no `title:` at all.
- **Document titles:** none carry dates. Many entries have no title (1237/doc6, 1291/doc13, 18 and 21, eight in 689, all of 188), so the sidebar falls back to long H1 headings.
- **Order:** 146 puts two analysis pages ahead of Document 1, and 689 puts `amt-decree` ahead of Document 1.
- **Later documents:** 139 and 146 group them under `other-docs`; no other folder has such a group.
- **Orphans:** 19 pages are in no toc: 13 in 689, 4 in 188 and 2 in 1237.

## Best folder: 139

Its `index.md` is the only landing page that tells a layman, in order, what the file is about, who is involved, the outcome and the timeline. It opens with two plain paragraphs (the widow's 1824 petition and the 1849 sale before emigration), then a facts table, then a dated timeline. Its document pages also carry dates in their headings and nearly all open with a summary.

| Folder | Landing page now | Main gap |
|---|---|---|
| 139 | Overview, facts table, timeline | Timeline stops at 1824; the 1849 sale is missing |
| 1237 | Regency background, then a 10-step narrative | Timeline table starts at Document 3; no facts table |
| 689 | Regency background, then a timeline | Never says plainly what the case is; 13 orphan pages |
| 146 | Argument that there were two Jobst Heinrichs | Identity analysis, not a case overview; no timeline |
| 1291 | "TODO" | No overview; almost no page summaries |
| 147 | Three sentences | No facts table or timeline |
| 188 | Pointer to 146 | Documents untitled; `doc5` unfinished |

## Recommendations

1. **139:** extend the timeline through September 1849, add a `title:` in the toc, and rename "Other Documents" to "Sale Documents (1849)".
2. **1237:** move the regency section to "Rentkammer Explained". Rebuild the timeline as one row per event starting 29 May 1798, with a link to each document. Fold the ten narrative sections into the document pages.
3. **689:** replace the opening with two paragraphs on the debt to Hempel & Söhne and the 200 Reichsthaler loan. Keep the timeline. Move `amt-decree` and the service slip into a "Background documents" group, and put the numbering and analysis pages in a final "Supplementary notes" group or delete them.
4. **146:** move the two-Jobst-Heinrichs argument to its own page at the end, together with the two Document 1 analyses. Write a 139-style overview covering 1808–1810 and the 1850 sale.
5. **1291:** write the overview from scratch. It has three petitioners (Krückeberg, Vogt, Brüggemann), so the timeline needs a "Party" column.
6. **147:** nest `doc5` under `content`, add the facts table, and say in the overview that only Document 5 is transcribed.
7. **188:** keep it short, add the facts table and toc titles, and either finish or drop `doc5`, `3-right` and `last-page`.
8. **All folders:** use one chapter title form, "Subject, No. X Berenbusch (years)", and one document title form, "Type of document (date)".

## Errors found along the way

- **`139/other-docs.md`:** says the sale was in 1850 and its table caption says no. 18; the pages it lists are dated 1849 and concern no. 10.
- **`139/content.md`:** says the documents are from 1822; they are from 1824.
- **`1237/content.md`:** the English link for item 2 points to `doc3.md`, and item 3 is dated 1800 where the index says 1799.
- **`146/content.md`:** item 2 links to `doc1.md` and item 11 links to `doc10.md`.

`claude-case-file-analysis.md` in the repository already recommends the same pattern, but its description of the current state is out of date (it mentions `intro.md` and `timeline.md` pages that no longer exist).

Which folder should I restructure first? I suggest 1237, since its content already exists and
only needs rearranging.
