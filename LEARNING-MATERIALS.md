# Learning Materials

> This guide lives at the project root so it stays tracked by git.
> The `learning-materials/` folder itself is **gitignored** — paste your raw files there freely.

---

## Folder Layout

```
learning-materials/
  <slug>/          ← one subfolder per material, matching temp/progress/<slug>/
    <your files>
```

| What you have               | Where to put it                                                                                                                 |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| A PDF book or paper         | `learning-materials/<slug>/<book>.pdf`                                                                                          |
| A slide deck                | `learning-materials/<slug>/<deck>.pptx` (export `.ppt` or Keynote decks to `.pptx` or PDF first)                                |
| A Word document             | `learning-materials/<slug>/<doc>.docx`                                                                                          |
| A long video or recording   | `learning-materials/<slug>/<video>.mp4`; put `<video>.srt` or `.vtt` next to it if you have captions, which skips transcription |
| A YouTube video or playlist | Nothing to download: give the agent the link                                                                                    |
| A web article               | Nothing to download: give the agent the link (it saves the article as Markdown)                                                 |
| A course folder or ZIP      | `learning-materials/<slug>/` (any structure; files are ordered by name)                                                         |

---

## Adding a New Material

1. Create a subfolder `learning-materials/<your-slug>/` and drop your files in. Skip this for links, or for files you'd rather leave where they are.
2. Tell the **Study Agent** `add <path or link>`, or run:
   ```
   /add-material <path | folder | zip | URL>
   ```
3. The agent extracts the text into `learning-materials/<slug>/_extracted/` with page, slide, or timestamp markers, detects the structure (PDF bookmarks, chapter headings, slide sections, YouTube chapters, or ~10-minute video parts), and shows it to you to confirm or edit.
4. It then creates:
   - `temp/progress/<slug>/manifest.json`: progress tracker and structure
   - `temp/progress/<slug>/session-log.md` and `spotlight-log.md`
   - `temp/Notes/<slug>/overview.md`: a one-page overview listing every unit with its location and status
5. If no structure can be detected, paste the table of contents when asked.

---

## Naming Convention

Use a short, lowercase, hyphenated slug that is **consistent** across:

```
learning-materials/<slug>/       ← raw files (gitignored)
learning-materials/<slug>/_extracted/  ← generated text + outline (gitignored)
temp/progress/<slug>/            ← progress tracking (gitignored)
temp/Notes/<slug>/               ← overview, notes, Q&A log, summaries (gitignored)
```

The agent derives the slug from the title (`Designing Data-Intensive Applications` → `designing-data-intensive-applications`); you can then refer to the material by any short part of its name.

---

## Progress & Notes Files (per material)

| File                                                  | Location                                | Purpose                                                                                      |
| ----------------------------------------------------- | --------------------------------------- | -------------------------------------------------------------------------------------------- |
| `<name>.txt`, `<name>.outline.json`                   | `learning-materials/<slug>/_extracted/` | Extracted text with location markers, and the detected structure                             |
| `manifest.json`                                       | `temp/progress/<slug>/`                 | Source of truth: progress, resume point, structure, concepts, questions, quizzes             |
| `session-log.md`                                      | `temp/progress/<slug>/`                 | Chronological log of all tracked sessions                                                    |
| `spotlight-log.md`                                    | `temp/progress/<slug>/`                 | Log of standalone deep-dive sessions                                                         |
| `overview.md`                                         | `temp/Notes/<slug>/`                    | One-page overview: At a Glance, every unit with location and status, Study Goals, Key Themes |
| `<N>-<ch>-<concept>.md`                               | `temp/Notes/<slug>/`                    | Concept notes saved via `/save-note`                                                         |
| `qa-log.md`                                           | `temp/Notes/<slug>/`                    | Questions answered from the material via `/ask-material`                                     |
| `<slug>-ch<N>-summary.md`, `<slug>-<unit>-summary.md` | `temp/Notes/<slug>/summary/`            | Chapter or unit summaries via `/summarize-chapter` (optional `.pdf`)                         |
| `<slug>-full-summary.md`                              | `temp/Notes/<slug>/summary/`            | Whole-material summary via `/summarize-chapter <slug> all`                                   |

---

## Session Types

| Type          | Start with                      | Saves to                                                |
| ------------- | ------------------------------- | ------------------------------------------------------- |
| **Tracked**   | `/start-study`, or say "resume" | `manifest.json` after every unit, plus `session-log.md` |
| **Deep Dive** | `/deep-dive`                    | `spotlight-log.md` only (no progress change)            |

---

## Summaries

Generate a precise, cited summary at any time:

```
/summarize-chapter <slug> chapter: <N>               ← one chapter (.md)
/summarize-chapter <slug> unit: <id>                 ← one section or video part
/summarize-chapter <slug> all                        ← every chapter + a full summary
/summarize-chapter <slug> chapter: <N> format: pdf   ← also a .pdf
```

Summaries are saved to `temp/Notes/<slug>/summary/` and don't affect progress. PDF export uses `markdown` and `weasyprint` in `.venv/`; on macOS, WeasyPrint also needs `brew install pango`.
